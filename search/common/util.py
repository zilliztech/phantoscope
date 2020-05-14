import os
import urllib.request
import urllib.error
import urllib.parse
import errno
import tarfile
import base64
from common.error import DecodeError, DownloadFileError
from common.config import ALLOWED_IMAGE_EXTENSIONS


def save_tmp_file(name, file_data=None, url=None):
    DEFAULT_PATH = "./tmp/"
    extension = "jpg"
    if file_data:
        try:
            img_data = file_data.split(",")
            if len(img_data) == 2:
                posting = img_data[0]
                data_type = posting.split("/")[1]
                extension = data_type.split(";")[0]
                encode_method = data_type.split(";")[1]
                if encode_method != "base64":
                    raise DecodeError("Encode method not base64")
                imgstring = img_data[1]
            else:
                imgstring = img_data[0]
            with open(DEFAULT_PATH + name + "." + extension, "wb") as f:
                f.write(base64.b64decode(imgstring))
            return DEFAULT_PATH + name + "." + extension
        except Exception as e:
            raise DecodeError("Decode string error", e)
    if url:
        try:
            urllib.request.urlretrieve(url, DEFAULT_PATH + name + "." + extension)
            return DEFAULT_PATH + name + "." + extension
        except Exception as e:
            raise DownloadFileError("Download file from url %s" % url, e)
    return None
