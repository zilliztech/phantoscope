import os
import time
import logging
import uuid
import urllib.request
import urllib.error
import urllib.parse
import numpy as np
from numpy import linalg as LA
import tensorflow as tf
from keras.applications.xception import Xception as KerasXception
from keras.applications.xception import preprocess_input as preprocess_input_xception
from keras.preprocessing import image
import base64
import keras.backend.tensorflow_backend as KTF

LOCAL_TMP_PATH = os.getenv("UPLOAD_FOLDER", "/tmp/")


class Xception:
    def __init__(self):
        self.input_shape = (299, 299, 3)
        self.weight = 'imagenet'
        self.pooling = 'avg'
        self.load_config()

    def load_config(self):
        # read model config from environment
        self.device_str = os.environ.get("device_id", "/cpu:0")
        self.user_config = tf.ConfigProto(allow_soft_placement=False)
        gpu_mem_limit = float(os.environ.get("gpu_mem_limit", 0.3))
        self.user_config.gpu_options.per_process_gpu_memory_fraction = gpu_mem_limit
        self.user_config.gpu_options.allow_growth = True
        if os.environ.get("log_device_placement", False):
            self.user_config.log_device_placement = True
        print("device id %s, gpu memory limit: %f" %
              (self.device_str, gpu_mem_limit))

        self.graph = tf.Graph()
        with self.graph.as_default():
            with tf.device(self.device_str):
                self.session = tf.Session(config=self.user_config, graph=self.graph)
                KTF.set_session(self.session)
                self.model = KerasXception(weights=self.weight,
                                           input_shape=(self.input_shape[0],
                                                        self.input_shape[1],
                                                        self.input_shape[2]),
                                           pooling=self.pooling,
                                           include_top=False)
                self.graph = KTF.get_graph()
                self.session = KTF.get_session()
                self.model.trainable = False
                self.model.predict(np.zeros(
                    (1, self.input_shape[0], self.input_shape[1], 3)))
                self.graph.as_default()
                self.session.as_default()

    def extract_feature(self, img_path):
        img = image.load_img(
            img_path,
            target_size=(
                self.input_shape[0],
                self.input_shape[1]))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input_xception(img)
        with self.graph.as_default():
            with self.session.as_default():
                # with tf.device(self.device_str):
                feat = self.model.predict(img)

        norm_feat = feat[0] / LA.norm(feat[0])
        norm_feat = [i.item() for i in norm_feat]
        return norm_feat

    @property
    def name(self):
        return "xception"

    @property
    def type(self):
        return "encoder"

    @property
    def input(self):
        return "image"

    @property
    def output(self):
        return "vector"

    @property
    def dimension(self):
        return "2048"

    @property
    def metric_type(self):
        return "L2"


def save_tmp_file(name, file_data=None, url=None):
    extension = 'jpg'
    file_path = os.path.join(LOCAL_TMP_PATH, name + '.' + extension)
    if file_data:
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
        file_path = os.path.join(LOCAL_TMP_PATH, name + '.' + extension)
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(imgstring))
    if url:
        try:
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            logging.error(
                "Download file from url error : %s",
                str(e),
                exc_info=True)
            raise
            # raise DownloadFileError("Download file from url %s" % url, e)
    return file_path


def run(xception, images, urls):
    vectors = []
    start = time.time()
    if images:
        for img in images:
            file_name = "{}-{}".format("processor", uuid.uuid4().hex)
            image_path = save_tmp_file(file_name, file_data=img)
            vector = xception.extract_feature(image_path)
            vectors.append(vector)
    else:
        for url in urls:
            file_name = "{}-{}".format("processor", uuid.uuid4().hex)
            image_path = save_tmp_file(file_name, url=url)
            if image_path:
                vector = xception.extract_feature(image_path)
                vectors.append(vector)
    end = time.time()
    logging.info('%s cost: {:.3f}s'.format(end - start), "xception")
    return vectors
