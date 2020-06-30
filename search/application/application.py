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


import json
import logging
from models.application import Application as DB
from models.application import insert_application, search_application, del_application, update_application
from common.error import NotExistError
from common.error import RequestError
from common.error import ArgsCheckError
from common.error import ExistError
from storage.storage import S3Ins, MilvusIns
from storage.storage import MongoIns
from application.mapping import new_mapping_ins
from application.utils import fields_check, fields2dict
from models.fields import insert_fields, search_fields, delete_fields
from models.fields import Fields as FieldsDB
from pipeline.pipeline import pipeline_detail
from operators.client import identity
from operators.operator import operator_detail

logger = logging.getLogger(__name__)


class Application():
    def __init__(self, name, fields, buckets):
        self._application_name = name
        self._fields = fields
        self._buckets = buckets

    @property
    def name(self):
        return self._application_name

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, fields):
        self._fields = fields

    @property
    def buckets(self):
        return self._buckets

    @buckets.setter
    def buckets(self, buckets):
        self._buckets = buckets

    def save(self):
        fields = json.dumps(self._fields)
        app = DB(name=self._application_name, fields=fields, s3_buckets=self._buckets)
        try:
            # Record created resource
            # TODO create s3 bucket if bucket not exist
            S3Ins.new_s3_buckets(self.buckets.split(","))
            # TODO create milvus collections
            insert_application(app)
            logger.info("create new application %s", self.name)
        except Exception as e:
            logger.error(e)
            # TODO collection created resource
            raise e
        return self


def all_applications():
    res = []
    try:
        apps = search_application()
        for x in apps:
            fields = search_fields(json.loads(x.Application.fields))
            app = Application(name=x.Application.name, fields=fields2dict(fields), buckets=x.Application.s3_buckets)
            res.append(app)
        logger.info("get all application")
        return res
    except Exception as e:
        logger.error(e)
        raise e


def application_detail(name):
    try:
        x = search_application(name)
        if not x:
            raise NotExistError(f"application {name} not exist", "")
        fields = search_fields(json.loads(x.fields))
        app = Application(name=x.name, fields=fields2dict(fields), buckets=x.s3_buckets)
        return app
    except Exception as e:
        logger.error(e)
        raise e


def create_milvus_collections_by_fields(app):
    for field in search_fields(app.fields):
        if field.type == "pipeline":
            pipe = pipeline_detail(field.value)
            name = pipe.encoder.get("name")
            instance_name = pipe.encoder.get("instance")
            encoder = operator_detail(name)
            instance = encoder.inspect_instance(instance_name)
            ei = identity(instance.endpoint)
            MilvusIns.new_milvus_collection(f"{app.name}_{name}_{instance_name}", int(ei["dimension"]), 1024, "l2")


def new_application(app_name, fields, s3_buckets):
    ok, message = fields_check(fields)
    if not ok:
        raise ArgsCheckError(message, "")
    try:
        # check application exist
        if search_application(app_name):
            raise ExistError(f"application <{app_name}> had exist", "")
        # insert fields to metadata
        fieldsdb = []
        for name, field in fields.items():
            fieldsdb.append(FieldsDB(name=name, type=field.get('type'),
                                     value=field.get('value'), app=app_name))
        ids = insert_fields(fieldsdb)
        # create a application entity collection
        MongoIns.new_mongo_collection(f"{app_name}_entity")
        app = Application(name=app_name, fields=ids, buckets=s3_buckets)
        # create milvus collections
        create_milvus_collections_by_fields(app)
        # insert application to metadata
        app.save()
        app.fields = fields2dict(search_fields(ids))
        return app
    except Exception as e:
        logger.error("error happen during create app: %s", str(e), exc_info=True)
        raise e


def delete_milvus_collections_by_fields(app):
    for _, field in app.fields.items():
        if field["type"] == "pipeline":
            pipe = pipeline_detail(field["value"])
            name = pipe.encoder.get("name")
            instance_name = pipe.encoder.get("instance")
            MilvusIns.del_milvus_collection(f"{app.name}_{name}_{instance_name}")


def delete_application(name):
    try:
        if len(entities_list(name, 100)):
            raise RequestError("Prevent to delete application with entity not deleted", "")
        # TODO rewrite clean all resource before change metadata
        x = del_application(name)
        if not x:
            raise NotExistError(f"application {name} not exist", "")
        x = x[0]
        fields = search_fields(json.loads(x.fields))
        app = Application(name=x.name, fields=fields2dict(fields), buckets=x.s3_buckets)
        delete_milvus_collections_by_fields(app)
        delete_fields(json.loads(x.fields))
        S3Ins.del_s3_buckets(x.s3_buckets.split(","))
        MongoIns.delete_mongo_collection(f"{name}_entity")
        logger.info("delete application %s", name)
        return app
    except Exception as e:
        logger.error(e)
        raise e


def entities_list(name, num):
    res = []
    try:
        docs = MongoIns.list_documents(f"{name}_entity", num)
        for doc in docs:
            res.append(new_mapping_ins(docs=doc))
        logger.info("get application %s entity list", name)
        return res
    except Exception as e:
        logger.error(e)
        raise e


def delete_entity(app_name, entity_id):
    try:
        mongo_ins_name = f"{app_name}_entity"
        entity = MongoIns.search_by_id(mongo_ins_name, entity_id)
        if not entity.count():
            raise NotExistError("Entity %s not exist" % entity_id, "NotExistError")
        res_en = []
        for item in entity:
            en = new_mapping_ins(item)
            res_en.append(en)
            for name, fields in en._docs.items():
                # delete s3 object
                bucket_name = fields.get("url").split("/")[-2]
                object_name = fields.get("url").split("/")[-1]
                S3Ins.del_object(bucket_name, object_name)
                # delete vector from milvus
                vids = fields.get("ids")
                pipe = pipeline_detail(name)
                instance_name = pipe.encoder.get("instance")
                MilvusIns.del_vectors(f"{app_name}_{name}_{instance_name}", vids)
            # delete from mongo
            MongoIns.delete_by_id(mongo_ins_name, entity_id)
        logger.info("delete entity %s in application %s", entity_id, app_name)
        return res_en
    except Exception as e:
        logger.error(e)
        raise e
