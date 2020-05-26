import base64
import getopt
import json
import logging
import os
import sys
import requests
import multiprocessing
import time
from itertools import islice, takewhile, repeat

logging.basicConfig(level=logging.INFO)
data_dir = "/tmp/256_ObjectCategories"
server_addr = "127.0.0.1:5000"
app_name = "example"
pipeline_name = None


def get_app_body_fields(app_name):
    global server_addr
    url = "http://%s/v1/application/%s" % (server_addr, app_name)
    try:
        reply = requests.get(url)
        content = json.loads(reply.content)
        application_feilds = content["_fields"]
        return application_feilds
    except Exception as e:
        logging.error("request url %s error: %s", url, str(e), exc_info=True)
        raise e


def get_pipeline_field(all_fields, pipeline_name):
    for field_name, value in all_fields.items():
        if value.get("type", None) == 'object':
            if (not pipeline_name) or value.get("pipeline") == pipeline_name:
                return field_name
            else:
                continue
    err_msg = "Can not find pipeline %s in app %s" % (pipeline_name, app_name)
    logging.error(err_msg)
    raise Exception(err_msg)


def get_app_field_name(app_name, pipeline_name=None):
    app_fileds = get_app_body_fields(app_name)
    image_field = get_pipeline_field(app_fileds, pipeline_name)
    return image_field


def construt_request_body(image_field, base64_image):
    template_data = {
        "fields": {
            image_field: {
                "data": base64_image
            }
        },
        "targetFields": {
            "data": base64_image
        }
    }
    return template_data


def get_file_num(data_path):
    num = 0
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".jpg"):
                num += 1
    return num


def get_file_generator(data_path):
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".jpg"):
                yield os.path.join(root, file)


def upload_image(file_num, file_generator, field_name):
    success_count, fail_count = 0, 0

    start = time.time()
    for img in file_generator:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = str(encoded_string, encoding='utf-8')
            data = construt_request_body(field_name, encoded_string)

            r = requests.post(upload_url, json=data)
            if r.status_code == 200:
                success_count += 1
            else:
                fail_count += 1
                logging.warning("Upload file '%s' error due to: %s" % (img, r.content))
            logging.debug("success: {} fail: {} total: {}".format(
                success_count, fail_count, file_num))

    logging.info("All data has been uploaded: \n"
                 "success: {} fail: {} total: {}".format(
        success_count, fail_count, file_num))
    end = time.time()
    logging.info('upload %d images cost: {:.3f}s'.format(end - start), file_num)


def parallel_upload(file_num, file_generator, field_name, batch_size):
    split_every = (lambda n, it:
                   takewhile(bool, (list(islice(it, n)) for _ in repeat(None))))
    core = 8
    start = time.time()
    with multiprocessing.Pool(processes=core) as pool:
        pool_list = []
        splited_list = split_every(batch_size, iter(file_generator))
        for tmp_list in splited_list:
            num = len(tmp_list)
            pool_list.append(pool.apply_async(upload_image, (num, tmp_list, field_name)))
        [res.get() for res in pool_list]
    end = time.time()
    logging.info('upload %d images cost: {:.3f}s'.format(end - start), file_num)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], '-h-d:-s:-a:-p:',
                               ['help', 'data_path=', "server=", 'app_name', 'pipeline_name'])
    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            logging.info("[*] Help info")
            exit()
        if opt_name in ('-s', '--server'):
            server_addr = opt_value
            logging.info("[*] Server address:port is %s", server_addr)
            continue
        if opt_name in ('-d', '--data_path'):
            data_dir = opt_value
            logging.info("[*] Data directory is %s", data_dir)
            continue
        if opt_name in ('-a', '--app_name'):
            app_name = opt_value
            logging.info("[*] Application name is %s", app_name)
            continue
        if opt_name in ('-p', '--pipeline_name'):
            pipeline_name = opt_value
            logging.info("[*] Pipeline name is %s", pipeline_name)
            continue

    upload_url = "http://%s/v1/application/%s/upload" % (server_addr, app_name)
    logging.info("upload url is %s", upload_url)

    image_field_name = get_app_field_name(app_name, pipeline_name)
    file_num = get_file_num(data_dir)
    file_generator = get_file_generator(data_dir)
    parallel_upload(file_num, file_generator, image_field_name, 500)
