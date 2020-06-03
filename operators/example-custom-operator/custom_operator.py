import os
from utils import LOCAL_TMP_PATH, save_tmp_file


def model_data_dir():
    return os.path.abspath(os.path.join('.', 'data'))


class CustomOperator:
    def __init__(self):
        pass

    def run(self, images, urls):
        raise NotImplementedError("Must implement run function entry")

    @property
    def name(self):
        raise NotImplementedError("Must define name")

    @property
    def type(self):
        raise NotImplementedError("Must define type")

    @property
    def input(self):
        raise NotImplementedError("Must define input")

    @property
    def output(self):
        raise NotImplementedError("Must define output")

    @property
    def dimension(self):
        raise NotImplementedError("Must define dimension")

    @property
    def metric_type(self):
        raise NotImplementedError("Must define metric_type")
