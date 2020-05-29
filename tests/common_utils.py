import os
import json
import uuid
import time
import logging
import base64
import random
import math
import cv2
import requests
from matplotlib import pyplot as plt

server_addr = "127.0.0.1:5000"
global_show_search_result = True


def register_operator(endpoint, operator_name):
    url = "http://%s/v1/operator/regist" % server_addr
    payload = {
        "endpoint": endpoint,
        "name": operator_name
    }
    payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def create_pipeline(pipeline_name, encoder_name="vgg16", processors=""):
    url = "http://%s/v1/pipeline/%s" % (server_addr, pipeline_name)
    payload = {
        "input": "image",
        "description": "this is a test pipeline description",
        "processors": processors,
        "encoder": encoder_name,
        "indexFileSize": 1024,
    }
    payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def create_app(app_name, pipeline_name, image_field_name):
    url = "http://%s/v1/application/%s" % (server_addr, app_name)
    payload = dict(fields={})
    payload["fields"]["name"] = {"type": "str", "value": "defalut name"}
    payload["fields"]["upload_time"] = {"type": "str", "value": "defalut time str"}
    payload["fields"][image_field_name] = {"type": "object", "pipeline": pipeline_name}
    payload["s3Buckets"] = str(uuid.uuid1())
    payload = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def delete_application(app_name):
    url = "http://%s/v1/application/%s" % (server_addr, app_name)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("DELETE", url, headers=headers)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def delete_pipeline(pipeline_name):
    url = "http://%s/v1/pipeline/%s" % (server_addr, pipeline_name)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("DELETE", url, headers=headers)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def delete_operator(operator_name):
    url = "http://%s/v1/operator/%s" % (server_addr, operator_name)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("DELETE", url, headers=headers)
    reply = json.loads(response.text)
    if isinstance(reply, dict) and reply.get('error'):
        logging.error("some errors occur: %s", response.text)
    else:
        logging.debug(response.text)


def search(app_name, image_field_name, image_folder,
           search_times=2, topk=5, nprob=12, if_show=False):
    url = "http://%s/v1/application/%s/search" % (server_addr, app_name)
    payload = dict(fields={})
    payload["fields"]["name"] = {"type": "str", "value": "defalut name"}
    payload["fields"]["upload_time"] = {"type": "str", "value": str(time.time())}
    payload["fields"][image_field_name] = {"data": ''}
    payload["topk"] = topk
    payload["nprobe"] = nprob

    headers = {'Content-Type': 'application/json'}
    image_list = []
    for _, _, files in os.walk(image_folder):
        for file in files:
            if file.endswith(".jpg"):
                image_file = os.path.join(image_folder, file)
                image_list.append(image_file)
    start = time.time()
    for i in range(search_times):
        id = random.randint(0, len(image_list) - 1)
        image_file = image_list[id]
        with open(image_file, "rb") as image:
            encoded_string = base64.b64encode(image.read())
            encoded_string = str(encoded_string, encoding='utf-8')
            payload["fields"][image_field_name]['data'] = encoded_string
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            if response.status_code == 500:
                raise Exception("search status 500")
                # logging.error("search status 500")

            reply = json.loads(response.text)
            if isinstance(reply, dict) and reply.get('error'):
                raise Exception("some errors occur: %s" % response.text)
                # logging.error("some errors occur: %s", response.text)
            assert len(reply) <= topk, "get %d search results, expect %d results" % (len(reply), topk)
            if if_show and topk < 12:
                display_result(image_file, reply)
            logging.debug("id: %d, response %s", id, response.text)

    end = time.time()
    logging.debug('search %d times cost: {:.3f}s'.format(end - start), search_times)


def url2cv(url):
    image_path = 'url.jpg'
    data = requests.get(url)
    with open(image_path, 'wb') as file:
        file.write(data.content)

    return cv2.imread(image_path)


def display_result(search_image, reply):
    num = len(reply) + 1

    sqrt_res = math.sqrt(num)
    row = math.ceil(sqrt_res)
    col = math.ceil(sqrt_res)
    plt.figure(figsize=(20, 16))
    plt.subplot(row, col, 1)
    plt.title("raw image for search", fontsize=20)
    img = cv2.imread(search_image)
    img = img[:, :, ::-1]
    plt.imshow(img)

    for i in range(0, num - 1):
        img_url = reply[i].get('_image_url')
        img = url2cv(img_url)
        plt.subplot(row, col, i + 2)
        plt.title("top %d" % (i + 1), fontsize=20)
        plt.imshow(img[:, :, ::-1])
    plt.show()


def upload(app_name, image_field_name, test_images_folder):
    url = "http://%s/v1/application/%s/upload" % (server_addr, app_name)
    payload = dict(fields={})
    # payload["fields"]["name"] = {"type": "str", "value": "defalut name"}
    # payload["fields"]["upload_time"] = {"type": "str", "value": "defalut time str"}
    payload["fields"][image_field_name] = {"data": ''}
    headers = {'Content-Type': 'application/json'}
    start = time.time()
    file_num = 0
    for _, _, files in os.walk(test_images_folder):
        for file in files:
            if file.endswith(".jpg"):
                file_num += 1
                image_file = os.path.join(test_images_folder, file)
                with open(image_file, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    encoded_string = str(encoded_string, encoding='utf-8')
                    payload["fields"][image_field_name]['data'] = encoded_string
                    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
                    logging.debug(response.text)
    end = time.time()
    logging.info('upload %d images cost: {:.3f}s'.format(end - start), file_num)
