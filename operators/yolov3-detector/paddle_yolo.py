import os
import uuid
import base64
import logging
import urllib.request
import time
import numpy as np
import yaml
import cv2
import paddle.fluid as fluid
from yolo_infer import offset_to_lengths
from yolo_infer import coco17_category_info, bbox2out
from yolo_infer import Preprocess


def temp_directory():
    return os.path.abspath(os.path.join('.', 'data'))


COCO_MODEL_PATH = os.path.join(temp_directory(), "yolov3_darknet")
YOLO_CONFIG_PATH = os.path.join(COCO_MODEL_PATH, "yolo.yml")
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


class YOLO_v3:
    def __init__(self):
        self.model_init = False
        self.user_config = self.get_operator_config()
        self.model_path = COCO_MODEL_PATH
        self.config_path = YOLO_CONFIG_PATH
        with open(self.config_path) as f:
            self.conf = yaml.safe_load(f)

        self.infer_prog, self.feed_var_names, self.fetch_targets = fluid.io.load_inference_model(
            dirname=self.model_path,
            executor=self.executor,
            model_filename='__model__',
            params_filename='__params__')
        self.clsid2catid, self.catid2name = coco17_category_info(False)
        self.execute(np.zeros((300, 300, 3), dtype='float32'))

    def get_operator_config(self):
        try:
            config = {}
            self.device_str = os.environ.get("device_id", "/cpu:0")
            if "gpu" not in self.device_str.lower():
                self.place = fluid.CPUPlace()
            else:
                gpu_device_id = int(self.device_str.split(':')[-1])
                gpu_mem_limit = float(os.environ.get("gpu_mem_limit", 0.3))
                os.environ['FLAGS_fraction_of_gpu_memory_to_use'] = str(
                    gpu_mem_limit)
                config["gpu_memory_limit"] = gpu_mem_limit
                self.place = fluid.CUDAPlace(gpu_device_id)
            self.executor = fluid.Executor(self.place)
            return config
        except Exception as e:
            logging.error("unexpected error happen during read config",
                          exc_info=True)
            raise e

    def get_bboxes(self, bbox_results, threshold=0.5):
        bboxes = [[]]
        for item in bbox_results:
            box, score, cls = item["bbox"], item["score"], item["category_id"]
            idx = item["image_id"]
            if score > threshold:
                assert idx == 0, "get_bboxes function now must input image = 1"
                bboxes[idx].append(BoundingBox(x1=box[0], y1=box[1],
                                               x2=box[0] + box[2],
                                               y2=box[1] + box[3],
                                               score=score,
                                               label=self.catid2name[int(cls)]))
        return bboxes

    @staticmethod
    def get_obj_image(images, bboxes):
        obj_images = []
        for i, frame_bboxes in enumerate(bboxes):
            frame_object = []
            for j, bbox in enumerate(frame_bboxes):
                tmp_obj = images[i][int(bbox.y1):int(
                    bbox.y2), int(bbox.x1):int(bbox.x2)]
                frame_object.append(cv2base64(tmp_obj))
            obj_images.append(frame_object)
        return obj_images

    def execute(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        img_data = Preprocess(image,
                              self.conf['arch'],
                              self.conf['Preprocess'])
        data_dict = {k: v for k, v in zip(self.feed_var_names, img_data)}
        outs = self.executor.run(self.infer_prog,
                                 feed=data_dict,
                                 fetch_list=self.fetch_targets,
                                 return_numpy=False)
        out = outs[-1]
        lod = out.lod()
        lengths = offset_to_lengths(lod)
        np_data = np.array(out)

        res = {'bbox': (np_data, lengths), 'im_id': np.array([[0]])}
        bbox_results = bbox2out([res], self.clsid2catid, False)
        bboxes = self.get_bboxes(bbox_results, 0.5)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        objs = self.get_obj_image([image], bboxes)
        return objs[0]

    def bulk_execute(self, images):
        objs = []
        for image in images:
            objs.append(self.execute(image))
        return objs

    @property
    def name(self):
        return "paddle_yolo"

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
                    result_images.append(detector.execute(image))
        else:
            for url in urls:
                file_name = "{}-{}".format("processor", uuid.uuid4().hex)
                image_path = save_tmp_file(file_name, url=url)
                if image_path:
                    image = cv2.imread(image_path)
                    result_images.append(detector.execute(image))
    except Exception as e:
        logging.error("something error: %s", str(e), exc_info=True)
    end = time.time()
    logging.info('%s cost: {:.3f}s, get %d results'.format(end - start),
                 "yolov3 detector", len(result_images))
    return result_images
