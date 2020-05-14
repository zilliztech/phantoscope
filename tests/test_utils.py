import pytest
from common.utils import save_tmp_file
from common.error import DecodeError, DownloadFileError


def test_save_tmp_file():
    url = ""
    data = ""
