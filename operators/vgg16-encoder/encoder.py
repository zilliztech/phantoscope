import os
import uuid
import time
import logging
import urllib.request, urllib.error, urllib.parse
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as preprocess_input_vgg
from keras.preprocessing import image
import numpy as np
from numpy import linalg as LA
import base64


class Vgg:
    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model_vgg = VGG16(weights=self.weight,
                               input_shape=(self.input_shape[0],
                                            self.input_shape[1],
                                            self.input_shape[2]),
                               pooling=self.pooling,
                               include_top=False)
        self.model_vgg.predict(np.zeros((1, 224, 224, 3)))

    @property
    def name(self):
        return "vgg16"

    @property
    def type(self):
        return "encoder"

    @property
    def dimension(self):
        return "512"

    @property
    def accept_filetype(self):
        return ["png", "jpg", "jepg"]

    @property
    def input(self):
        return "image"

    @property
    def output(self):
        return "vector"

    @property
    def metric_type(self):
        return "L2"

    def extract_feature(self, img_path):
        img = image.load_img(img_path,
                             target_size=(self.input_shape[0],
                                          self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_vgg(img)
        feat = self.model_vgg.predict(img)
        norm_feat = feat[0] / LA.norm(feat[0])
        norm_feat = [i.item() for i in norm_feat]
        return norm_feat


LOCAL_TMP_PATH = os.getenv("UPLOAD_FOLDER", "/tmp/")


def save_from_url(path, name, url):
    try:
        start = time.time()
        urllib.request.urlretrieve(url, path + name + ".jpg")
        end = time.time()
        logging.info('  save_tmp_file cost: {:.3f}s'.format(end - start))
        return path + name + ".jpg"
    except Exception:
        return ""


def save_from_base64(name, file_data=None):
    extension = "jpg"
    try:
        img_data = file_data.split(",")
        if len(img_data) == 2:
            posting = img_data[0]
            data_type = posting.split("/")[1]
            extension = data_type.split(";")[0]
            encode_method = data_type.split(";")[1]
            if encode_method != "base64":
                logging.error("Encode method not base64")
                raise
                # raise DecodeError("Encode method not base64")
            imgstring = img_data[1]
        else:
            imgstring = img_data[0]
        with open(LOCAL_TMP_PATH + name + "." + extension, "wb") as f:
            f.write(base64.b64decode(imgstring))
        return LOCAL_TMP_PATH + name + "." + extension
    except Exception as e:
        # raise DecodeError("Decode string error", e)
        return ""


def run(vgg, images, urls):
    vectors = []
    start = time.time()
    if images:
        for img in images:
            file_name = "{}-{}".format("processor", uuid.uuid4().hex)
            image_path = save_from_base64(file_name, img)
            vector = vgg.extract_feature(image_path)
            vectors.append(vector)
    else:
        for url in urls:
            file_name = "{}-{}".format("processor", uuid.uuid4().hex)
            image_path = save_from_url(LOCAL_TMP_PATH, file_name, url)
            if image_path:
                vector = vgg.extract_feature(image_path)
                vectors.append(vector)
    end = time.time()
    logging.info('%s cost: {:.3f}s, get %d results'.format(end - start),
                 "vgg16", len(vectors))
    return vectors
