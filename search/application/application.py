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


import logging
from resource.resource import Resource
from common.error import NotExistError
from common.error import RequestError
from common.error import ArgsCheckError
from common.error import ExistError
from common.const import APPLICATION_COLLECTION_NAME, PIPELINE_COLLECTION_NAME
from storage.storage import S3Ins, MilvusIns
from storage.storage import MongoIns
from application.mapping import new_mapping_ins
from application.utils import fields_check
from pipeline.pipeline import pipeline_detail
from operators.client import identity


logger = logging.getLogger(__name__)


class Application(Resource):
    def __init__(self, name, fields, bucket):
        self.name = name
        self.fields = fields
        self.bucket = bucket
        self.metadata = None


def all_applications():
    res = []
    try:
        apps = MongoIns.list_documents(APPLICATION_COLLECTION_NAME, 0)
        for x in apps:
            app = Application(name=x["name"], fields=x["fields"], bucket=x["bucket"])
            app.metadata = x["metadata"]
            res.append(app)
        logger.info("get all application")
        return res
    except Exception as e:
        logger.error(e)
        raise e


def application_detail(name):
    try:
        app = MongoIns.search_by_name(APPLICATION_COLLECTION_NAME, name)
        if not app:
            raise NotExistError(f"application {name} not exist", "")
        app = app[0]
        application = Application(app["name"], app["fields"], app["bucket"])
        application.metadata = app["metadata"]
        return application
    except Exception as e:
        logger.error(e)
        raise e


def new_application(app_name, fields, s3_bucket):
    ok, message = fields_check(fields)
    if not ok:
        raise ArgsCheckError(message, "")
    try:
        # check application exist
        if MongoIns.search_by_name(APPLICATION_COLLECTION_NAME, app_name):
            raise ExistError(f"application <{app_name}> had exist", "")
    except ExistError:
        raise
    try:
        for _, value in fields.items():
            if value.get("type") == "pipeline":
                pipe = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, value.get("value"))[0]
                ei = identity(pipe.get("encoder").get("instance").get("endpoint"))
                name = f"{app_name}_{pipe.get('encoder').get('instance').get('name').replace('phantoscope_', '')}"
                MilvusIns.new_milvus_collection(name, int(ei["dimension"]), 1024, "l2")
        # create a application entity collection
        MongoIns.new_mongo_collection(f"{app_name}_entity")
        S3Ins.new_s3_buckets(s3_bucket)
        # create milvus collections
        app = Application(name=app_name, fields=fields, bucket=s3_bucket)
        app.metadata = app._metadata()
        MongoIns.insert_documents(APPLICATION_COLLECTION_NAME, app.to_dict())
        return app
    except Exception as e:
        logger.error("error happen during create app: %s", str(e), exc_info=True)
        raise e


def delete_milvus_collections_by_fields(app):
    for _, field in app['fields'].items():
        if field["type"] == "pipeline":
            pipe = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, field.get("value"))[0]
            name = f"{app.get('name')}_{pipe.get('encoder').get('instance').get('name').replace('phantoscope_', '')}"
            MilvusIns.del_milvus_collection(name)


def delete_application(name, force=False):
    try:
        if not force:
            if not entities_list(name, 100, 0):
                raise RequestError("Prevent to delete application with entity not deleted", "")
        app = MongoIns.search_by_name(APPLICATION_COLLECTION_NAME, name)
        if not app:
            raise NotExistError(f"application {name} not exist", "")
        app = app[0]
        delete_milvus_collections_by_fields(app)
        S3Ins.del_s3_buckets(app['bucket'])
        MongoIns.delete_mongo_collection(f"{name}_entity")
        MongoIns.delete_by_name(APPLICATION_COLLECTION_NAME, name)
        logger.info("delete application %s", name)
        application = Application(app["name"], app["fields"], app["bucket"])
        application.metadata = app["metadata"]
        return application
    except Exception as e:
        logger.error(e)
        raise e


def entities_list(name, num, page):
    res = []
    try:
        docs = MongoIns.list_documents(f"{name}_entity", num, page)
        for doc in docs:
            res.append(new_mapping_ins(docs=doc))
        logger.info("get application %s entity list", name)
        return res
    except Exception as e:
        logger.error(e)
        raise e


def count_entities(name):
    try:
        count = MongoIns.count_documents(f"{name}_entity")
        logger.info(f"get count of application {name} entities")
        return str(count)
    except Exception as e:
        logger.error(e)
        raise e


def delete_entity(app_name, entity_id):
    try:
        mongo_ins_name = f"{app_name}_entity"
        entity = MongoIns.search_by_id(mongo_ins_name, entity_id)

        if not entity.count():
            raise NotExistError("Entity %s not exist" % entity_id, "NotExistError")
        for item in entity:
            en = new_mapping_ins(item)
            for name, fields in en._docs.items():
                # delete s3 object
                bucket_name = fields.get("url").split("/")[-2]
                object_name = fields.get("url").split("/")[-1]
                S3Ins.del_object(bucket_name, object_name)
                # delete vector from milvus
                vids = fields.get("ids")
                app = application_detail(app_name)
                pipe_name = app.fields[name]["value"]
                pipe = pipeline_detail(pipe_name)
                instance_name = pipe.encoder.get("instance")
                MilvusIns.del_vectors(f"{app_name}_{name}_{instance_name}", vids)
            # delete from mongodb
            MongoIns.delete_by_id(mongo_ins_name, entity_id)
            logger.info("delete entity %s in application %s", entity_id, app_name)
            return en
    except Exception as e:
        logger.error(e)
        raise e
