import pytest


def create_pipeline():
    pass


def create_application():
    pass


def create_operator():
    pass


def delete_application():
    pass


def delete_pipeline():
    pass


def delete_operator():
    pass


def search():
    pass


def upload():
    pass


def test_object_app():
    create_operator()
    create_pipeline()
    create_application()

    search()  # none
    upload()
    search()  # same
    search()  # none

    delete_application()
    delete_pipeline()
    delete_operator()


def test_face_app():
    pass
