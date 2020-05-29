import pytest
from common_utils import *

logging.basicConfig(level=logging.INFO)
# some test_info which may be gotten by some query command.
# now hard-code in local
host_ip = "192.168.2.3"
vgg_port = 50001
face_detector_port = 50005
face_encoder_port = 50004
# ensure all face images exist a well-detected face
face_images_folder = os.path.join(os.getcwd(), "99.face")
dogs_images_folder = os.path.join(os.getcwd(), "056.dog")
giraffe_images_folder = os.path.join(os.getcwd(), "084.giraffe")


@pytest.fixture()
def vgg_app():
    operator_endpoint = "%s:%d" % (host_ip, vgg_port)
    operator_name = "vgg16"
    pipeline_name = "vgg_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "vgg_app"

    register_operator(operator_endpoint, operator_name)
    create_pipeline(pipeline_name, operator_name)
    create_app(app_name, pipeline_name, image_field_name)

    yield

    delete_application(app_name)
    delete_pipeline(pipeline_name)
    delete_operator(operator_name)


@pytest.fixture()
def face_app():
    operator_endpoint1 = "%s:%d" % (host_ip, face_detector_port)
    operator_endpoint2 = "%s:%d" % (host_ip, face_encoder_port)
    operator_name1 = "face_detector"
    operator_name2 = "face_embedding"
    pipeline_name = "face_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "face_app"

    register_operator(operator_endpoint1, operator_name1)
    register_operator(operator_endpoint2, operator_name2)
    create_pipeline(pipeline_name, encoder_name=operator_name2, processors=operator_name1)
    create_app(app_name, pipeline_name, image_field_name)

    yield

    delete_application(app_name)
    delete_pipeline(pipeline_name)
    delete_operator(operator_name1)
    delete_operator(operator_name2)


def test_object_app(vgg_app):
    pipeline_name = "vgg_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "vgg_app"

    with pytest.raises(Exception) as e:
        search(app_name, image_field_name, giraffe_images_folder, if_show=global_show_search_result)

    upload(app_name, image_field_name, dogs_images_folder)
    search(app_name, image_field_name, dogs_images_folder, if_show=global_show_search_result)
    search(app_name, image_field_name, giraffe_images_folder, if_show=global_show_search_result)


# @pytest.mark.skip(reason='test images do not exist')
def test_face_app(face_app):
    pipeline_name = "face_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "face_app"

    with pytest.raises(Exception) as e:
        search(app_name, image_field_name, face_images_folder, if_show=global_show_search_result)
    upload(app_name, image_field_name, face_images_folder)
    # error due to no face detected, maybe this need to be adjusted
    with pytest.raises(Exception) as e:
        search(app_name, image_field_name, dogs_images_folder, if_show=global_show_search_result)
    search(app_name, image_field_name, face_images_folder, if_show=global_show_search_result)


def test_none_search():
    operator_endpoint = "%s:%d" % (host_ip, vgg_port)
    operator_name = "none_vgg16"
    pipeline_name = "none_vgg_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "none_app"
    none_app_name = "none_app_none"

    register_operator(operator_endpoint, operator_name)
    create_pipeline(pipeline_name, operator_name)
    create_app(app_name, pipeline_name, image_field_name)

    # search before upload
    logging.debug("search in a nonexistent app with no images1")
    with pytest.raises(Exception) as e:
        search(none_app_name, image_field_name, giraffe_images_folder)

    logging.debug("search in a nonexistent app with no images2")
    with pytest.raises(Exception) as e:
        search(none_app_name, image_field_name, dogs_images_folder)
    logging.debug("search in an existent app with no images1")
    with pytest.raises(Exception) as e:
        search(app_name, image_field_name, giraffe_images_folder)
    logging.debug("search in an existent app with no images2")
    with pytest.raises(Exception) as e:
        search(app_name, image_field_name, dogs_images_folder)

    upload(app_name, image_field_name, dogs_images_folder)

    # search after upload
    logging.debug("search in an existent app1, normal search")
    search(app_name, image_field_name, giraffe_images_folder)
    logging.debug("search in an existent app2, normal search")
    search(app_name, image_field_name, dogs_images_folder)

    logging.debug("search in a nonexistent app")
    with pytest.raises(Exception) as e:
        search(none_app_name, image_field_name, dogs_images_folder)

    logging.debug("search in an existent app, randmon topk&nprob")
    topk = random.randint(1, 90)
    nprob = random.randint(1, 1000)
    search(app_name, image_field_name, dogs_images_folder, topk=topk, nprob=nprob)

    delete_application(app_name)
    delete_pipeline(pipeline_name)
    delete_operator(operator_name)


def test_search_topk():
    operator_endpoint = "%s:%d" % (host_ip, vgg_port)
    operator_name = "topk_vgg16"
    pipeline_name = "topk_vgg_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "topk_app"

    register_operator(operator_endpoint, operator_name)
    create_pipeline(pipeline_name, operator_name)
    create_app(app_name, pipeline_name, image_field_name)

    upload(app_name, image_field_name, dogs_images_folder)

    logging.debug("search in an existent app, correct topk")
    for i in range(1, 100):
        nprob = random.randint(1, 100)
        search(app_name, image_field_name, dogs_images_folder, topk=i, nprob=nprob)
        search(app_name, image_field_name, giraffe_images_folder, topk=i, nprob=nprob)

    logging.debug("search in an existent app, negative topk")
    for i in range(-10, 0):
        nprob = random.randint(1, 1000)
        with pytest.raises(Exception) as e:
            search(app_name, image_field_name, dogs_images_folder, topk=i, nprob=nprob)

    delete_application(app_name)
    delete_pipeline(pipeline_name)
    delete_operator(operator_name)


def test_search_nprobe():
    operator_endpoint = "%s:%d" % (host_ip, vgg_port)
    operator_name = "nprobe_vgg16"
    pipeline_name = "nprobe_vgg_pipeline"
    image_field_name = pipeline_name + "_image"
    app_name = "nprobe_app"

    register_operator(operator_endpoint, operator_name)
    create_pipeline(pipeline_name, operator_name)
    create_app(app_name, pipeline_name, image_field_name)

    upload(app_name, image_field_name, dogs_images_folder)

    logging.debug("search in an existent app, correct nprob")
    for i in range(1, 100):
        topk = random.randint(1, 100)
        search(app_name, image_field_name, dogs_images_folder, topk=topk, nprob=i)
        search(app_name, image_field_name, giraffe_images_folder, topk=topk, nprob=i)

    logging.debug("search in an existent app, negative nprob")
    for i in range(-10, 1):
        nprob = random.randint(1, 1000)
        search(app_name, image_field_name, dogs_images_folder, topk=nprob, nprob=i)

    delete_application(app_name)
    delete_pipeline(pipeline_name)
    delete_operator(operator_name)
