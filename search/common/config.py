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

MINIO_ADDR = os.getenv("MINIO_ADDR", "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRECT_KEY", "minioadmin")
MINIO_1ST_BUCKET = os.getenv("1ST_BUCKET", "alpha")
MINIO_BUCKET_NUM = os.getenv("MINIO_OBJ_LIMIT", 20)

MONGO_ADDR = os.getenv("MONGO_ADDR", "127.0.0.1")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_USERNAME = os.getenv("MONGO_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWD", "passwd")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "tmp/video")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", {"gif", "jpg", "jpeg", "png"})

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}

LOCAL_CACHE_PATH = "./tmp"
LOCAL_TMP_PATH = "/tmp"

STAGE_EXTRACT = "extract"
STAGE_PREDICT = "predict"
ALL_STAGE = [STAGE_EXTRACT, STAGE_PREDICT]

MILVUS_ADDR = os.getenv("MILVUS_ADDR", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

SEARCH_MAGIC_NUM = os.getenv("SEARCH_MAGIC_NUM", 6)
SEARCH_COUNT_NUM = os.getenv("SEARCH COUNT NUM", 3)


#--------------
META_DATABASE_ENDPOINT = os.getenv("SEARCH_IMAGES_DATABASE_EP", "mysql://root:passwd@127.0.0.1:3306/search")
META_DATABASE_USERNAME = os.getenv("SEARCH_IMAGES_DATABASE_USERNAME", "root")
META_DATABASE_PASSWD = os.getenv("SEARCH_IMAGES_DATABASE_PASSWD", "passwd")
META_DATABASE_NAME = os.getenv("SEARCH_IMAGES_DATABASE_NAME", "search")

DEFAULT_RUNTIME = "docker"
