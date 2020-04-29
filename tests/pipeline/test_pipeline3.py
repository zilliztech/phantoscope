import pytest
from pipeline.pipeline import run_pipeline, Pipeline
import time
from operators.operator import regist_operators

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    # when first run or need to fresh operators
    # regist_operators()
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


@pytest.fixture(name="url")
def pipeline_def2():
    url = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1585317988584&di=73113a2b2e3f98195944ded43a4cb2e7&imgtype=0&src=http%3A%2F%2Ff.hiphotos.baidu.com%2Fzhidao%2Fpic%2Fitem%2F8d5494eef01f3a2930f397239b25bc315c607c27.jpg"
    return url


# depend on thirdparty/facenet
def test_face(url):
    p = Pipeline(name="face", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face detection and embedding",
                 processors=["mtcnn_detect_face"], encoder="face_embedding")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 128


def test_ssd_xception(url):
    p = Pipeline(name="pic_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with ssd and embed them with xception",
                 processors=["ssd"], encoder="xception")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 2048


# depend on thirdparty/maskrcnn
def test_mask_rcnn_xception(url):
    p = Pipeline(name="make_rcnn_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with mask-rcnn and embed them with xception",
                 processors=["mask_rcnn"], encoder="xception")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 2048


# depend on thirdparty/maskrcnn
def test_mask_rcnn_vgg(url):
    p = Pipeline(name="make_rcnn_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="detect object with mask-rcnn and embed them with vgg",
                 processors=["mask_rcnn"], encoder="vgg")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 512


# depend on thirdparty/facenet & thirdparty/rude-carnie
def test_face_gender(url):
    p = Pipeline(name="face_gender", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face gender",
                 processors=["mtcnn_detect_face"], encoder="gender_embedding")
    res = run_pipeline(p, data=None, url=url)
    # assert len(res[-1]) == 2


# depend on thirdparty/facenet & thirdparty/rude-carnie
def test_face_age(url):
    p = Pipeline(name="face_gender", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="face age",
                 processors=["mtcnn_detect_face"], encoder="age_embedding")
    res = run_pipeline(p, data=None, url=url)
    # assert len(res[-1]) == 8


def test_pic_xception(url):
    p = Pipeline(name="pic_xception", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="pic xception",
                 processors=[], encoder="xception")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 2048


# yolo implemented by paddlepaddle
def test_yolo_vgg(url):
    p = Pipeline(name="yolo vgg", input="", output="", dimension="",
                 index_file_size="", metric_type="",
                 description="yolo vgg",
                 processors=["paddle_yolo"], encoder="vgg")
    res = run_pipeline(p, data=None, url=url)
    assert len(res[-1]) == 512
