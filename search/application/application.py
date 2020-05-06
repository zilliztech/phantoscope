import json
import logging
from models.application import Application as DB
from models.application import insert_application, search_application, del_application, update_application
from models.mapping import search_by_application, search_from_mapping, del_mapping
from pipeline.pipeline import _all_pipelines
from common.error import NotExistError
from common.error import RequestError
from storage.storage import S3Ins, MilvusIns
from application.mapping import new_mapping_ins


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
            S3Ins.new_s3_buckets(self.buckets.split(","))
            insert_application(app)
            logger.info("create new application %s", self.name)
        except Exception as e:
            logger.error(e)
            raise e
        return self


def all_applications():
    res = []
    try:
        apps = search_application()
        for x in apps:
            fields = json.loads(x.Application.fields)
            app = Application(name=x.Application.name, fields=fields, buckets=x.Application.s3_buckets)
            res.append(app)
        logger.info("get all application")
        return res
    except Exception as e:
        logger.error(e)
        return e


def application_detail(name):
    try:
        x = search_application(name)
        if not x:
            raise NotExistError(f"application {name} not exist", "")
        fields = json.loads(x.fields)
        app = Application(name=x.name, fields=fields, buckets=x.s3_buckets)
        return app
    except Exception as e:
        logger.error(e)
        return e


def new_application(name, fields, s3_buckets):
    app = Application(name=name, fields=fields, buckets=s3_buckets)
    try:
        all_pipelines_names = [x.name for x in _all_pipelines()]
        for _, v in fields.items():
            if v.get("type") == "object":
                if v.get("pipeline") not in all_pipelines_names:
                    return NotExistError("pipeline not exist", "pipeline %s not exist" % v.get("value"))
            if v.get("type") != "object":
                if "value" not in v:
                    return RequestError("key 'value' not exist", "request error")
        return app.save()
    except Exception as e:
        return e


def delete_application(name):
    try:
        x = del_application(name)
        if not x:
            raise NotExistError("application %s not exist" % name, "")
        x = x[0]
        fields = json.loads(x.fields)
        app = Application(name=x.name, fields=fields, buckets=x.s3_buckets)
        S3Ins.del_s3_buckets(x.s3_buckets.split(","))
        logger.info("delete application %s", name)
        return app
    except Exception as e:
        logger.error(e)
        return e


def patch_application(name, fields, s3_buckets):
    try:
        app_model = DB(name=name, fields=json.dumps(fields), s3_buckets=s3_buckets)
        x = update_application(name, app_model)
        if not x:
            raise NotExistError(f"application {name} not exist", "")
        app = Application(name=x.name, fields=fields, buckets=s3_buckets)
        logger.info("change appication %s config", name)
        return app
    except Exception as e:
        logger.error(e)
        return e


def entities_list(name, num, page):
    res = []
    try:
        for i in search_by_application(name, num, num*page):
            res.append(new_mapping_ins(id=i.id, app_name=i.app_name,
                                       image_url=i.image_url,
                                       fields=i.fields, target_fields=i.target_fields))
        logger.info("get application %s entity list", name)
        return res
    except Exception as e:
        logger.error(e)
        return e


def delete_entity(app_name, entity_name):
    try:
        entity = search_from_mapping(entity_name)
        if not entity:
            raise NotExistError("Entity %s not exist" % entity_name, "NotExistError")
        MilvusIns.del_vectors(app_name, [int(entity_name)])
        bucket_name = entity.image_url.split("/")[-2]
        object_name = entity.image_url.split("/")[-1]
        S3Ins.del_object(bucket_name, object_name)
        del_mapping(entity_name)
        logger.info("delete entity %s in application %s", entity_name, app_name)
        return new_mapping_ins(
            id=entity.id, app_name=entity.app_name, image_url=entity.image_url,
            fields=entity.fields, target_fields=entity.target_fields
        )
    except Exception as e:
        logger.error(e)
        return e
