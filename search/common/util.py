import os
import urllib.request
import urllib.error
import urllib.parse
import errno
import tarfile
import base64
from common.error import DecodeError, DownloadFileError
from common.config import ALLOWED_IMAGE_EXTENSIONS

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def temp_directory():
    path = os.path.expanduser('~/.tmp/resources')
    mkdir_p(path)
    return path


def download_temp_file(url, local_path=None, untar=False):
    if local_path is None:
        local_path = url.rsplit('/', 1)[-1]
    local_path = os.path.join(temp_directory(), local_path)
    mkdir_p(os.path.dirname(local_path))
    if not os.path.isfile(local_path):
        print('Downloading {:s} to {:s}...'.format(url, local_path))
        f = urllib.request.urlopen(url)
        with open(local_path, 'wb') as local_f:
            local_f.write(f.read())

        if untar:
            with tarfile.open(local_path) as tar_f:
                tar_f.extractall(temp_directory())
    if untar:
        return temp_directory()
    return local_path


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
