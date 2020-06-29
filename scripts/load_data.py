import base64
import json
import logging
import os
import argparse
import multiprocessing
import time
import math
from itertools import islice, takewhile, repeat
from tqdm import tqdm
import requests

error_log = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload_error.log')
logging.basicConfig(level=logging.WARNING, filename=error_log, filemode='w+')

accept_ends = ['bmp', 'jpg', 'jpeg', 'png']


def get_app_body_fields(address, app_name):
    url = "http://%s/v1/application/%s" % (address, app_name)
    try:
        reply = requests.get(url)
        content = json.loads(reply.content)
        application_feilds = content["_fields"]
        return application_feilds
    except Exception as e:
        logging.error("request url %s error: %s", url, str(e), exc_info=True)
        raise e


def get_app_field_name(address, app_name, pipeline_name=None):
    all_fields = get_app_body_fields(address, app_name)
    for field_name, value in all_fields.items():
        if value.get("type", None) == 'pipeline':
            if (not pipeline_name) or value.get("value") == pipeline_name:
                return field_name
            else:
                continue
    err_msg = "Can not find pipeline %s in app %s" % (pipeline_name, app_name)
    logging.error(err_msg)
    raise Exception(err_msg)


def construt_request_body(image_field, base64_image):
    template_data = {
        "fields": {
            image_field: {
                "data": base64_image
            }
        }
    }
    return template_data


def get_file_num(data_path):
    num = 0
    for root, dirs, files in os.walk(data_path):
        for file in files:
            extension = file.split('.')[-1]
            if extension in accept_ends:
                num += 1
    return num


def get_file_generator(data_path, file_max_num):
    i = 0
    for root, dirs, files in os.walk(data_path):
        for file in files:
            extension = file.split('.')[-1]
            if extension in accept_ends:
                i += 1
                if i > file_max_num: break
                yield os.path.join(root, file)


def upload_image(file_num, file_generator, field_name):
    success_count, fail_count = 0, 0

    start = time.time()
    for img in file_generator:
        with open(img, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = str(encoded_string, encoding='utf-8')
            data = construt_request_body(field_name, encoded_string)
            try:
                r = requests.post(upload_url, json=data)
                if r.status_code == 200:
                    success_count += 1
                else:
                    fail_count += 1
                    logging.warning("Upload file '%s' error due to: %s" % (img, r.content))
                logging.debug("success: {} fail: {} total: {}".format(
                    success_count, fail_count, file_num))
            except Exception as e:
                logging.error("Upload file '%s' error due to: %s" % (img, str(e)))

    logging.info("Data in this task has been uploaded: \n"
                 "success: {} fail: {} total: {}".format(
        success_count, fail_count, file_num))
    end = time.time()
    logging.info('upload %d images cost: {:.3f}s'.format(end - start), file_num)
    return (success_count, fail_count)


def parallel_upload(file_num, file_generator, field_name, batch_size=500, pool_num=12):
    split_every = (lambda n, it:
                   takewhile(bool, (list(islice(it, n)) for _ in repeat(None))))
    start = time.time()
    with multiprocessing.Pool(processes=pool_num) as pool:
        pool_list = []
        splited_list = split_every(batch_size, iter(file_generator))
        for tmp_list in splited_list:
            num = len(tmp_list)
            pool_list.append(pool.apply_async(upload_image, (num, tmp_list, field_name)))

        # sum all result
        success_cnt = 0
        failed_cnt = 0
        with tqdm(total=file_num) as pbar:
            for res in pool_list:
                tmp_sucess, tmp_failed = res.get()
                pbar.update(tmp_sucess + tmp_failed)
                success_cnt += tmp_sucess
                failed_cnt += tmp_failed

    end = time.time()
    print('upload %d images cost: {:.3f}s'.format(end - start) % file_num)
    return success_cnt, failed_cnt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--app_name", type=str, help='assigned app name',
                        dest='app_name', default='example')
    parser.add_argument("-p", "--pipeline_name", type=str, help='assigned pipeline name',
                        dest='pipeline_name', default=None)
    parser.add_argument("-d", "--data_path", type=str, help='assigned data path',
                        dest='data_dir')
    parser.add_argument("-s", "--server", type=str, help='assigned search api address',
                        dest='server_addr', default='127.0.0.1:5000')
    parser.add_argument("--batch_size", type=int, help='batch size each process upload',
                        dest='batch_size', default=500)
    parser.add_argument("--pool_num", type=int, help='number of multiprocessing pool',
                        dest='pool_num', default=4)
    args = parser.parse_args()

    upload_url = "http://%s/v1/application/%s/upload" % (args.server_addr, args.app_name)
    batch_size = args.batch_size
    pool_num = args.pool_num
    print("upload url is %s" % upload_url)

    image_field_name = get_app_field_name(args.server_addr, args.app_name, args.pipeline_name)
    file_num = get_file_num(args.data_dir)
    file_generator = get_file_generator(args.data_dir, file_num)
    # ensure run in all processes in the pool
    batch_size = min(math.ceil(file_num / pool_num), batch_size)

    print("allocate %d processes to load data, each task including %d images" % (pool_num, batch_size))
    print("Now begin to load image data and upload to phantoscope: ...")
    time.sleep(0.1)

    sucess_cnt, failed_cnt = parallel_upload(file_num, file_generator, image_field_name, batch_size, pool_num)

    print("All images has been uploaded: success {}, fail {}".format(sucess_cnt, failed_cnt))
    print("Please read file '%s' to check upload_error log." % error_log)
