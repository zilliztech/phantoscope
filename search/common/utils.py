# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under the License.


import os
import urllib.request
import urllib.error
import urllib.parse
import base64
from common.error import DecodeError, DownloadFileError


def save_tmp_file(name, file_data=None, url=None):
    DEFAULT_PATH = os.path.abspath('./tmp/')
    extension = "jpg"
    file_path = os.path.join(DEFAULT_PATH, name + "." + extension)
    if file_data:
        try:
            img_data = file_data.split(",")
            if len(img_data) == 2:
                posting = img_data[0]
                data_type = posting.split("/")[1]
                extension = data_type.split(";")[0]
                encode_method = data_type.split(";")[1]
                if encode_method != "base64":
                    raise DecodeError("Encode method not base64", Exception())
                imgstring = img_data[1]
            else:
                imgstring = img_data[0]
            file_path = os.path.join(DEFAULT_PATH, name + "." + extension)
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(imgstring))
            return file_path
        except Exception as e:
            raise DecodeError("Decode string error", e)
    if url:
        try:
            urllib.request.urlretrieve(url, file_path)
            return file_path
        except Exception as e:
            raise DownloadFileError("Download file from url %s" % url, e)
    return None
