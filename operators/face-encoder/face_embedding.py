import base64
import logging
import os
import time
import urllib.request
import uuid
import cv2
import numpy as np
import tensorflow as tf
from facenet import prewhiten, get_model_filenames

LOCAL_TMP_PATH = "./tmp/"


def temp_directory():
    return os.path.abspath(os.path.join('.', 'data'))


class EmbedFaces:
    def __init__(self):
        self._minibatch = 5
        self.fetch_resources()
        self._model_dir = os.path.join(temp_directory(), '20170512-110547')
        self.images_placeholder = None
        self.init_config()

    def init_config(self):
        # read model config from environment
        self.device_str = os.environ.get("device_id", "/cpu:0")
        self.user_config = tf.ConfigProto(allow_soft_placement=True)
        gpu_mem_limit = float(os.environ.get("gpu_mem_limit", 0.3))
        self.user_config.gpu_options.per_process_gpu_memory_fraction = gpu_mem_limit
        self.user_config.gpu_options.allow_growth = True
        # for device debug info print
        if os.environ.get("log_device_placement", False):
            self.user_config.log_device_placement = True
        logging.info("device id %s, gpu memory limit: %f",
                     self.device_str, gpu_mem_limit)
        self.graph = tf.Graph()
        with self.graph.as_default():
            with tf.device(self.device_str):
                self.session = tf.Session(config=self.user_config, graph=self.graph)
                self.bulk_execute(np.zeros((1, 300, 300, 3)))

    def fetch_resources(self):
        # download_temp_file(MODEL_FILE, untar=True)
        pass

    def load_model(self):
        logging.info('[INFO] Loading model...')
        try:
            with self.graph.as_default():
                with tf.device(self.device_str):
                    with self.session.as_default():
                        model_path = self._model_dir
                        meta_file, ckpt_file = get_model_filenames(model_path)
                        saver = tf.train.import_meta_graph(
                            os.path.join(model_path, meta_file))
                        saver.restore(
                            self.session, os.path.join(
                                model_path, ckpt_file))

                        self.images_placeholder = self.graph.get_tensor_by_name('input:0')
                        self.embeddings = self.graph.get_tensor_by_name('embeddings:0')
                        self.phase_train_placeholder = self.graph.get_tensor_by_name('phase_train:0')
        except Exception as e:
            logging.error("[Error] Fail to load model due to %s", str(e), exc_info=True)
            # maybe raise a Exception here to interrupt this running
        else:
            logging.info('[INFO] Model loaded!')

    def execute(self, face_image):
        output_embs = self.bulk_execute([face_image])
        return output_embs[0]

    def bulk_execute(self, face_images):
        if self.images_placeholder is None:
            self.load_model()

        out_size = 160
        cleaned_images = []
        source_indices = []
        output_embs = [None for _ in face_images]

        for i, face_img in enumerate(face_images):
            [fh, fw] = face_img.shape[:2]
            if fh == 0 or fw == 0:
                output_embs[i] = np.zeros(128, dtype=np.float32)
            else:
                face_img = cv2.resize(face_img, (out_size, out_size))
                face_img = prewhiten(face_img)
                cleaned_images.append(face_img)
                source_indices.append(i)

        for k in range(0, len(cleaned_images), self._minibatch):
            embs = self.session.run(
                self.embeddings,
                feed_dict={
                    self.images_placeholder: cleaned_images[k: k + self._minibatch],
                    self.phase_train_placeholder: False
                })

            for emb, i in zip(embs, source_indices[k:k + self._minibatch]):
                output_embs[i] = emb.tolist()

        for l in output_embs:
            assert l is not None

        return output_embs

    @property
    def name(self):
        return "face_embedding"

    @property
    def type(self):
        return "encoder"

    @property
    def dimension(self):
        return "128"

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
            logging.error("Download file from url error : %s", str(e), exc_info=True)
            raise
            # raise DownloadFileError("Download file from url %s" % url, e)
    return file_path


def run(face_encoder, images, urls):
    vectors = []
    start = time.time()
    try:
        if images:
            for img in images:
                file_name = "{}-{}".format("processor", uuid.uuid4().hex)
                image_path = save_tmp_file(file_name, file_data=img)
                if image_path:
                    image = cv2.imread(image_path)
                    vectors.extend(face_encoder.bulk_execute([image]))
        else:
            for url in urls:
                file_name = "{}-{}".format("processor", uuid.uuid4().hex)
                image_path = save_tmp_file(file_name, url=url)
                if image_path:
                    image = cv2.imread(image_path)
                    vectors.extend(face_encoder.bulk_execute([image]))
    except Exception as e:
        logging.error("something error: %s", str(e), exc_info=True)
        pass
    end = time.time()
    logging.info('%s cost: {:.3f}s'.format(end - start), "face_embedding encoder")
    return vectors
