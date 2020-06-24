import os
import uuid
import logging
import base64
import urllib.request
import time
import numpy as np
import tensorflow as tf
import keras.backend.tensorflow_backend as KTF
import cv2
from mrcnn.config import Config
from mrcnn.model import MaskRCNN


def temp_directory():
    return os.path.abspath(os.path.join('.', 'data'))


MODEL_DIR = os.path.join(temp_directory())
COCO_MODEL_PATH = "mask_rcnn_coco.h5"
LOCAL_TMP_PATH = os.getenv("UPLOAD_FOLDER", "/tmp/")


class BoundingBox:
    def __init__(self, x1, y1, x2, y2, score, label=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.score = score
        self.label = label


class MaskRCNNConfig(Config):
    """Configuration for training on MS COCO.
        Derives from the base Config class and overrides values specific
        to the COCO dataset.
        """
    # Give the configuration a recognizable name
    NAME = "coco"

    # Number of classes (including background)
    NUM_CLASSES = 1 + 80  # COCO has 80 classes

    GPU_COUNT = 1

    IMAGES_PER_GPU = 1


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


class MaskRCNNDetectObject:
    def __init__(self):
        self.fetch_resources()
        self.model_init = False
        self.user_config = self.get_operator_config()
        # define special param here
        self.config = MaskRCNNConfig()
        self.label = [
            'BG',
            'person',
            'bicycle',
            'car',
            'motorcycle',
            'airplane',
            'bus',
            'train',
            'truck',
            'boat',
            'traffic light',
            'fire hydrant',
            'stop sign',
            'parking meter',
            'bench',
            'bird',
            'cat',
            'dog',
            'horse',
            'sheep',
            'cow',
            'elephant',
            'bear',
            'zebra',
            'giraffe',
            'backpack',
            'umbrella',
            'handbag',
            'tie',
            'suitcase',
            'frisbee',
            'skis',
            'snowboard',
            'sports ball',
            'kite',
            'baseball bat',
            'baseball glove',
            'skateboard',
            'surfboard',
            'tennis racket',
            'bottle',
            'wine glass',
            'cup',
            'fork',
            'knife',
            'spoon',
            'bowl',
            'banana',
            'apple',
            'sandwich',
            'orange',
            'broccoli',
            'carrot',
            'hot dog',
            'pizza',
            'donut',
            'cake',
            'chair',
            'couch',
            'potted plant',
            'bed',
            'dining table',
            'toilet',
            'tv',
            'laptop',
            'mouse',
            'remote',
            'keyboard',
            'cell phone',
            'microwave',
            'oven',
            'toaster',
            'sink',
            'refrigerator',
            'book',
            'clock',
            'vase',
            'scissors',
            'teddy bear',
            'hair drier',
            'toothbrush']
        self.model_path = os.path.join(temp_directory(), COCO_MODEL_PATH)
        # initialize model
        try:
            self.graph = tf.Graph()
            with self.graph.as_default():
                with tf.device(self.device_str):
                    self.session = tf.Session(config=self.user_config)
                    KTF.set_session(self.session)
                    self.rcnn = MaskRCNN(
                        mode="inference",
                        model_dir=MODEL_DIR,
                        config=self.config)
                    self.graph = KTF.get_graph()
                    self.session = KTF.get_session()
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
                config.log_device_placement = True
            logging.info("device id %s, gpu memory limit: %f",
                         self.device_str, gpu_mem_limit)

        except Exception as e:
            logging.error(
                "unexpected error happen during read config",
                exc_info=True)
            raise e
        logging.info("Model device str: %s, session config: %s",
                     self.device_str, config)
        return config

    def fetch_resources(self):
        # download_temp_file(COCO_MODEL_URL, COCO_MODEL_PATH)
        pass

    def load_model(self):
        self.rcnn.load_weights(self.model_path, by_name=True)
        self.model_init = True

    def get_bboxes(self, boxes, scores, classes):
        bboxes = [[
            BoundingBox(
                x1=box[1], y1=box[0], x2=box[3], y2=box[2], score=score, label=self.label[int(cls)])
            for (box, score, cls) in zip(boxes.tolist(), scores.tolist(), classes.tolist())
        ]]
        return bboxes

    @staticmethod
    def get_obj_image(images, bboxes):
        obj_images = []
        for i, frame_bboxes in enumerate(bboxes):
            frame_object = []
            for j, bbox in enumerate(frame_bboxes):
                tmp = images[i][int(bbox.y1):int(
                    bbox.y2), int(bbox.x1):int(bbox.x2)]
                frame_object.append(cv2base64(tmp))
            obj_images.append(frame_object)
        return obj_images

    def execute(self, image):
        with self.graph.as_default():
            with self.session.as_default():
                if not self.model_init:
                    self.load_model()
                results = self.rcnn.detect([image])
                bboxes = self.get_bboxes(
                    results[0]["rois"],
                    results[0]["scores"],
                    results[0]["class_ids"])
                bboxes[0].sort(key=lambda x: -x.score)
                objects_image = self.get_obj_image([image], bboxes)
                return objects_image[0]

    def bulk_execute(self, images):
        objs = []
        for image in images:
            objs.append(self.execute(image))
        return objs

    @property
    def name(self):
        return "mask_rcnn"

    @property
    def type(self):
        return "processor"

    @property
    def input(self):
        return "image"

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
            logging.error("Download file from url error : %s", str(e), exc_info=True)
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
    logging.info('%s cost: {:.3f}s, get %d results'.format(end - start),
                 "mask-rcnn detector", len(result_images))
    return result_images
