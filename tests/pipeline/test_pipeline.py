import pytest
import cv2
from pipeline.pipeline import run_pipeline, Pipeline
import time
from operators.operator import regist_operators
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    regist_operators()
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))


@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print('Signle test time cost: {:.3f}s'.format(time.time() - start))


@pytest.fixture(name="image")
def pipeline_def():
    image_path = "/home/abner/Desktop/test8.jpg"
    image = cv2.imread(image_path)
    return image


# depend on thirdparty/facenet
def test_face(image):
    p = Pipeline(name="face", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face detection and embedding",
                 processors=["mtcnn_detect_face"], encoder="face_embedding")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 128


def test_ssd_xception(image):
    p = Pipeline(name="pic_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with ssd and embed them with xception",
                 processors=["ssd"], encoder="xception")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 2048


# depend on thirdparty/maskrcnn
def test_mask_rcnn_xception(image):
    p = Pipeline(name="make_rcnn_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with mask-rcnn and embed them with xception",
                 processors=["mask_rcnn"], encoder="xception")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 2048


# depend on thirdparty/maskrcnn
def test_mask_rcnn_vgg(image):
    p = Pipeline(name="make_rcnn_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with mask-rcnn and embed them with vgg",
                 processors=["mask_rcnn"], encoder="vgg")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 512


# depend on thirdparty/facenet & thirdparty/rude-carnie
def test_face_gender(image):
    p = Pipeline(name="face_gender", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face gender",
                 processors=["mtcnn_detect_face"], encoder="gender_embedding")
    res = run_pipeline(p, image=image)
    # assert len(res[-1]) == 2


# depend on thirdparty/facenet & thirdparty/rude-carnie
def test_face_age(image):
    p = Pipeline(name="face_gender", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face age",
                 processors=["mtcnn_detect_face"], encoder="age_embedding")
    res = run_pipeline(p, image=image)
    # assert len(res[-1]) == 8


def test_pic_xception(image):
    p = Pipeline(name="pic_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="pic xception",
                 processors=[], encoder="xception")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 2048


# yolo implemented by paddlepaddle
def test_yolo_vgg(image):
    p = Pipeline(name="yolo vgg", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="yolo vgg",
                 processors=["paddle_yolo"], encoder="vgg")
    res = run_pipeline(p, image=image)
    assert len(res[-1]) == 512

# if __name__ == "__main__":
#     # face_pipeline1()
#     # pic_xception()
#     # ssd_xception()
#     # mask_rcnn_xception()
#     # mask_rcnn_vgg()
#     # face_gender()
#     # face_age()
#     yolo_vgg()
