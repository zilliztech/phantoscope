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
import pymongo
from bson.objectid import ObjectId
from milvus import Milvus, MetricType
from minio import Minio
from common.config import MILVUS_ADDR, MILVUS_PORT
from common.error import MilvusError, S3Error
from common.const import MINIO_BUCKET_PUBLIC_POLICY
from common.config import MINIO_ADDR, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from common.config import MONGO_ADDR, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD

logger = logging.getLogger(__name__)


class Storage:
    def __init__(self):
        pass


# code blow this comment need to be rewrite


type_mapping = {
    "l2": MetricType.L2
}


class MongoIns:
    @staticmethod
    def new_mongo_collection(name):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            db.create_collection(name)
        except Exception as e:
            raise e

    @staticmethod
    def delete_mongo_collection(name):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            db.drop_collection(name)
        except Exception as e:
            raise e

    @staticmethod
    def insert_documents(name, docs):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            id = getattr(db, name).insert_one(docs).inserted_id
            return id
        except Exception as e:
            raise e

    @staticmethod
    def list_documents(name, num, page):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            curso = getattr(db, name).find()
            res = curso.skip(num * page).limit(num)
            return res
        except Exception as e:
            raise e

    @staticmethod
    def count_documents(name):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            return getattr(db, name).count()
            # return getattr(db, name).find().count()
        except Exception as e:
            raise e

    @staticmethod
    def search_by_id(name, id):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            return getattr(db, name).find({"_id": ObjectId(id)}).limit(1)
        except Exception as e:
            raise e

    @staticmethod
    def search_by_vector_id(name, field_name, ids: list):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            res = getattr(db, name).find({f"{field_name}.ids": {"$in": ids}})
            return list(res)
        except Exception as e:
            raise e

    @staticmethod
    def delete_by_id(name, id):
        try:
            client = pymongo.MongoClient(MONGO_ADDR, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASSWORD)
            db = client.phantoscope
            return getattr(db, name).delete_many({"_id": ObjectId(id)})
        except Exception as e:
            raise e


class MilvusIns:
    @staticmethod
    def new_milvus_collection(name, dimension, index_file_size, metric_type):
        metric_type = type_mapping.get(metric_type, MetricType.L2)
        try:
            milvus = Milvus(host=MILVUS_ADDR, port=MILVUS_PORT)
            parma = {
                "collection_name": name,
                "dimension": dimension,
                "index_file_size": index_file_size,
                "metric_type": metric_type
            }
            res = milvus.create_collection(parma)
            if not res.OK():
                raise MilvusError("There was some error when create milvus collection", res)
        except Exception as e:
            raise MilvusError("There was some error when create milvus collection", e)

    @staticmethod
    def del_milvus_collection(name):
        try:
            milvus = Milvus(host=MILVUS_ADDR, port=MILVUS_PORT)
            res = milvus.drop_collection(collection_name=name)
            if not res.OK():
                raise MilvusError("There was some error when drop milvus collection", res)
        except Exception as e:
            err_msg = "There was some error when delete milvus collection"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise MilvusError(err_msg, e)

    @staticmethod
    def insert_vectors(name, vectors):
        try:
            milvus = Milvus(host=MILVUS_ADDR, port=MILVUS_PORT)
            res, ids = milvus.insert(collection_name=name, records=vectors)
            if not res.OK():
                err_msg = "There was some error when insert vectors"
                logger.error(f"{err_msg} : {str(res)}", exc_info=True)
                raise MilvusError(err_msg, res)
            return ids
        except Exception as e:
            err_msg = "There was some error when insert vectors"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise MilvusError(err_msg, e)

    @staticmethod
    def search_vectors(name, vector, topk, nprobe):
        search_param = {'nprobe': nprobe}
        try:
            milvus = Milvus(host=MILVUS_ADDR, port=MILVUS_PORT)
            res, ids = milvus.search(collection_name=name, query_records=vector, top_k=topk, params=search_param)
            if not res.OK():
                raise MilvusError("There was some error when search vectors", res)
            return ids
        except Exception as e:
            err_msg = "There was some error when search vectors"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise MilvusError(err_msg, e)

    @staticmethod
    def del_vectors(collection_name, ids):
        try:
            milvus = Milvus(host=MILVUS_ADDR, port=MILVUS_PORT)
            milvus.delete_entity_by_id(collection_name=collection_name, id_array=ids)
        except Exception as e:
            err_msg = "There was some error when delete vectors"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise MilvusError(err_msg, e)


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
            minio_client = cls.new_minio_client()
            for x in names:
                minio_client.make_bucket(x)
                minio_client.set_bucket_policy(x, json.dumps(gen_public_policy(x)))
        except Exception as e:
            err_msg = "There was some error when create s3 buckets"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise S3Error(err_msg, e)

    @classmethod
    def del_s3_buckets(cls, names):
        try:
            minio_client = cls.new_minio_client()
            for x in names:
                minio_client.remove_bucket(x)
        except Exception as e:
            err_msg = "There was some error when delete s3 buckets"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise S3Error(err_msg, e)

    @classmethod
    def upload2bucket(cls, bucket_name, file_path, file_name):
        try:
            minio_client = cls.new_minio_client()
            with open(file_path, 'rb') as f:
                file_stat = os.stat(file_path)
                minio_client.put_object(bucket_name, file_name, f, file_stat.st_size)
        except Exception as e:
            err_msg = "There was some error when put file to s3 buckets"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise S3Error(err_msg, e)

    @classmethod
    def del_object(cls, bucket_name, object_name):
        try:
            minio_client = cls.new_minio_client()
            minio_client.remove_object(bucket_name, object_name)
        except Exception as e:
            err_msg = "There was some error when delete object"
            logger.error(f"{err_msg} : {str(e)}", exc_info=True)
            raise S3Error(err_msg, e)


def gen_public_policy(name):
    prefix = "arn:aws:s3:::{}{}"
    policy = MINIO_BUCKET_PUBLIC_POLICY.copy()
    policy["Statement"][0]["Resource"] = [prefix.format(name, ""), prefix.format(name, "/*")]
    return policy
