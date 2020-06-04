import base64
import logging
import os
import time
from typing import Sequence
import urllib.request
import uuid
import cv2
import numpy as np
import tensorflow as tf
import align.detect_face

LOCAL_TMP_PATH = "./tmp/"


class BoundingBox:
    def __init__(self, x1, y1, x2, y2, score, label=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.score = score
        self.label = label


def cv2base64(image):
    try:
        tmp_file_name = os.path.join(LOCAL_TMP_PATH, "%s.jpg" % uuid.uuid1())
        cv2.imwrite(tmp_file_name, image)
        with open(tmp_file_name, "rb") as f:
            base64_data = base64.b64encode(f.read())
            base64_data = base64_data.decode("utf-8")
        return base64_data
    except Exception as e:
        err_msg = "Convert cv2 object to base64 failed: "
        logging.error(err_msg, e, exc_info=True)
        raise e


class MTCNNDetectFace:
    def __init__(self):
        self.fetch_resources()
        self.model_init = False
        self.user_config = self.get_operator_config()
        self.threshold = [0.45, 0.6, 0.7]
        self.factor = 0.709
        self.detection_window_size_ratio = .2

        try:
            self.graph = self.build_graph()
            with self.graph.as_default():
                with tf.device(self.device_str):
                    self.session = tf.Session(
                        config=self.user_config, graph=self.graph)
                    with self.session.as_default():
                        self.bulk_execute(np.zeros((1, 300, 300, 3)))
        except Exception as e:
            logging.error(
                "unexpected error happen during build graph",
                exc_info=True)
            raise e

    def get_operator_config(self):
        try:
            self.device_str = os.environ.get("device_id", "/cpu:0")
            config = tf.ConfigProto(allow_soft_placement=True)
            config.gpu_options.allow_growth = True
            gpu_mem_limit = float(os.environ.get("gpu_mem_limit", 0.3))
            config.gpu_options.per_process_gpu_memory_fraction = gpu_mem_limit
            # for device debug info print
            if os.environ.get("log_device_placement", False):
                self.user_config.log_device_placement = True
            logging.info("device id %s, gpu memory limit: %f",
                         self.device_str, gpu_mem_limit)

        except Exception as e:
            logging.error(
                "unexpected error happen during read config",
                exc_info=True)
            raise e
        logging.info(
            "Model device str: %s, session config: %s",
            self.device_str,
            config)
        return config

    def fetch_resources(self):
        pass

    def build_graph(self):
        self.pnet = None
        self.g = tf.Graph()
        return self.g

    def load_model(self):
        print('[INFO] Loading model...')
        with self.graph.as_default():
            with self.session.as_default():
                self.pnet, self.rnet, self.onet = align.detect_face.create_mtcnn(
                    self.session, os.path.dirname(align.__file__))
        print('[INFO] Model loaded!')

    @staticmethod
    def get_face_bboxes(images, detections) -> Sequence[Sequence[BoundingBox]]:
        vmargin = 0.2582651235637604
        hmargin = 0.3449094129917718

        batch_faces = []
        for img, bounding_boxes in zip(images, detections):
            if bounding_boxes is None:
                batch_faces.append([])
                continue
            frame_faces = []
            bounding_boxes = bounding_boxes[0]
            num_faces = bounding_boxes.shape[0]
            for i in range(num_faces):
                confidence = bounding_boxes[i][4]
                if confidence < .1:
                    continue

                img_size = np.asarray(img.shape)[0:2]
                det = np.squeeze(bounding_boxes[i][0:5])
                vmargin_pix = int((det[2] - det[0]) * vmargin)
                hmargin_pix = int((det[3] - det[1]) * hmargin)
                frame_faces.append(
                    BoundingBox(
                        x1=np.maximum(
                            det[0] - hmargin_pix / 2,
                            0) / img_size[1],
                        y1=np.maximum(
                            det[1] - vmargin_pix / 2,
                            0) / img_size[0],
                        x2=np.minimum(
                            det[2] + hmargin_pix / 2,
                            img_size[1]) / img_size[1],
                        y2=np.minimum(
                            det[3] + vmargin_pix / 2,
                            img_size[0]) / img_size[0],
                        score=det[4]))

            batch_faces.append(frame_faces)

        return batch_faces

    @staticmethod
    def get_face_images(images, bboxes):
        face_images = []
        for i, frame_bboxes in enumerate(bboxes):
            frame_faces = []
            [h, w] = images[i].shape[:2]
            for j, bbox in enumerate(frame_bboxes):
                tmp = images[i][int(bbox.y1 * h):int(bbox.y2 * h), int(bbox.x1 * w):int(bbox.x2 * w)]
                frame_faces.append(cv2base64(tmp))

            face_images.append(frame_faces)
        return face_images

    def execute(self, img):
        batch_frame_faces = self.bulk_execute([img])
        return batch_frame_faces[0]

    def bulk_execute(self, imgs):
        with self.graph.as_default():
            with tf.device(self.device_str):
                if self.pnet is None:
                    self.load_model()
                detections = align.detect_face.bulk_detect_face(
                    imgs, self.detection_window_size_ratio, self.pnet,
                    self.rnet, self.onet, self.threshold, self.factor)
                bboxes = self.get_face_bboxes(imgs, detections)
                batch_frame_faces = self.get_face_images(imgs, bboxes)
                return batch_frame_faces

    @property
    def name(self):
        return "mtcnn_detect_face"

    @property
    def type(self):
        return "processor"

    @property
    def input(self):
        return "image"

    @property
    def accept_filetype(self):
        return ["png", "jpg", "jepg"]

    @property
    def output(self):
        return "images"

    @property
    def dimension(self):
        return "-1"

    @property
    def metric_type(self):
        return "-1"


def save_tmp_file(name, file_data=None, url=None):
    start = time.time()
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
    end = time.time()
    logging.info('  save_tmp_file cost: {:.3f}s'.format(end - start))
    return file_path


def run(detector, images, urls):
    result_images = []
    start = time.time()
    try:
        if images:
            for img in images:
                file_name = "{}-{}".format("processor", uuid.uuid4().hex)
                image_path = save_tmp_file(file_name, file_data=img)
                if image_path:
                    image = cv2.imread(image_path)
                    result_images.extend(detector.bulk_execute([image]))
        else:
            for url in urls:
                file_name = "{}-{}".format("processor", uuid.uuid4().hex)
                image_path = save_tmp_file(file_name, url=url)
                if image_path:
                    image = cv2.imread(image_path)
                    result_images.extend(detector.bulk_execute([image]))
    except Exception as e:
        logging.error("something error: %s", str(e), exc_info=True)
        pass
    end = time.time()
    logging.info('%s cost: {:.3f}s'.format(end - start),
                 "face_detector detector")
    return result_images
