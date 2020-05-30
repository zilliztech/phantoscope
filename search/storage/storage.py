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
import json
import logging
from milvus import Milvus, MetricType
from minio import Minio
from common.config import MILVUS_ADDR, MILVUS_PORT
from common.error import MilvusError, S3Error
from common.const import MINIO_BUCKET_PUBLIC_POLICY
from common.config import MINIO_ADDR, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
logger = logging.getLogger(__name__)


class Storage:
    def __init__(self):
        pass
# code blow this comment need to be rewrite


type_mapping = {
    "l2": MetricType.L2
}


class MilvusIns:
    @staticmethod
    def new_milvus_collection(name, dimension, index_file_size, metric_type):
        metric_type = type_mapping.get(metric_type, MetricType.L2)
        milvus = Milvus()
        try:
            milvus.connect(MILVUS_ADDR, MILVUS_PORT)
            parma = {
                "collection_name": name,
                "dimension": dimension,
                "index_file_size": index_file_size,
                "metric_type": metric_type
            }
            res = milvus.create_collection(parma)
            if not res.OK():
                raise MilvusError("There has some error when create milvus collection", res)
        except Exception as e:
            raise MilvusError("There has some error when create milvus collection", e)

    @staticmethod
    def del_milvus_collection(name):
        milvus = Milvus()
        try:
            milvus.connect(MILVUS_ADDR, MILVUS_PORT)
            res = milvus.drop_collection(collection_name=name)
            if not res.OK():
                raise MilvusError("There has some error when drop milvus collection", res)
        except Exception as e:
            raise MilvusError("There has some error when delete milvus collection", e)

    @staticmethod
    def insert_vectors(name, vectors):
        milvus = Milvus()
        try:
            milvus.connect(MILVUS_ADDR, MILVUS_PORT)
            res, ids = milvus.insert(collection_name=name, records=vectors)
            if not res.OK():
                raise MilvusError("There has some error when insert vectors", res)
            return ids
        except Exception as e:
            logger.error("There has some error when insert vectors", exc_info=True)
            raise MilvusError("There has some error when insert vectors", e)

    @staticmethod
    def search_vectors(name, vector, topk, nprobe):
        milvus = Milvus()
        search_param = {'nprobe': nprobe}
        try:
            milvus.connect(MILVUS_ADDR, MILVUS_PORT)
            res, ids = milvus.search(collection_name=name, query_records=vector, top_k=topk, params=search_param)
            if not res.OK():
                raise MilvusError("There has some error when search vectors", res)
            return ids
        except Exception as e:
            raise MilvusError("There has some error when search vectors", e)

    @staticmethod
    def del_vectors(collection_name, ids):
        milvus = Milvus()
        try:
            milvus.connect(MILVUS_ADDR, MILVUS_PORT)
            milvus.delete_by_id(collection_name=collection_name, id_array=ids)
        except Exception as e:
            raise MilvusError("There has some error when delete vectors", e)


class S3Ins:
    @classmethod
    def new_minio_client(cls):
        return Minio(
            MINIO_ADDR,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

    @classmethod
    def new_s3_buckets(cls, names, region=None):
        try:
            minioClient = cls.new_minio_client()
            for x in names:
                minioClient.make_bucket(x)
                minioClient.set_bucket_policy(x, json.dumps(gen_public_policy(x)))
        except Exception as e:
            logger.error("There has some error when create s3 buckets", exc_info=True)
            raise S3Error("There has some error when create s3 buckets", e)

    @classmethod
    def del_s3_buckets(cls, names):
        try:
            minioClient = cls.new_minio_client()
            for x in names:
                minioClient.remove_bucket(x)
        except Exception as e:
            raise S3Error("There has some error when delete s3 buckets", e)

    @classmethod
    def upload2bucket(cls, bucket_name, file_path, file_name):
        try:
            minioClient = cls.new_minio_client()
            with open(file_path, 'rb') as f:
                file_stat = os.stat(file_path)
                minioClient.put_object(bucket_name, file_name, f, file_stat.st_size)
        except Exception as e:
            raise S3Error("There has some error when put file to s3 bucket", e)

    @classmethod
    def del_object(cls, bucket_name, object_name):
        try:
            minioClient = cls.new_minio_client()
            minioClient.remove_object(bucket_name, object_name)
        except Exception as e:
            raise S3Error("There has some error when delete object", e)


def gen_public_policy(name):
    prefix = "arn:aws:s3:::{}{}"
    policy = MINIO_BUCKET_PUBLIC_POLICY.copy()
    policy["Statement"][0]["Resource"] = [prefix.format(name, ""), prefix.format(name, "/*")]
    return policy
