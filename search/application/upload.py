import uuid
import time
import logging
from application.application import application_detail
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NotExistError
from storage.storage import MilvusIns, S3Ins
from models.mapping import Mapping as DB
from models.mapping import add_mapping_data
from application.mapping import new_mapping_ins
from common.config import MINIO_ADDR
from common.utils import save_tmp_file

logger = logging.getLogger(__name__)


def upload(name, **kwargs):
    try:
        app = application_detail(name)
        if not app:
            raise NotExistError("application not exist", "application %s not exist" % name)
        bucket_name = app.buckets.split(",")[0]
        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "object"]
        pipeline_fields = {x: y['pipeline'] for x, y in app.fields.items() if y.get('type') == "object"}
        new_fields = app.fields.copy()
        for k, v in kwargs.items():
            if k in accept_fields:
                new_fields[k]['value'] = v
        res = []
        for n, p in pipeline_fields.items():
            pipe = pipeline_detail(p)
            if not pipe:
                raise NotExistError("pipeline not exist", "pipeline %s not exist" % p)
            value = kwargs['fields'].get(n)
            file_data = value.get('data')
            url = value.get('url')
            file_name = "{}-{}".format(name, uuid.uuid4().hex)
            file_path = save_tmp_file(file_name, file_data, url)

            # begin to timing
            start = time.time()
            S3Ins.upload2bucket(bucket_name, file_path, file_name)
            upload_time = time.time()
            logger.debug("[timing] upload image to bucket costs: {:.3f}s".format(upload_time - start))

            vectors = run_pipeline(pipe, data=file_data, url=url)
            pipeline_time = time.time()
            logger.debug("[timing] run pipeline costs: {:.3f}s".format(pipeline_time - upload_time))

            milvus_collection_name = f"{pipe.name}_{pipe.encoder}"
            vids = MilvusIns.insert_vectors(milvus_collection_name, vectors)
            insert_time = time.time()
            logger.debug("[timing] insert to milvus costs: {:.3f}s".format(insert_time - pipeline_time))
            for vid in vids:
                m = DB(id=vid, app_name=name,
                       image_url=gen_url(bucket_name, file_name),
                       fields=new_fields)
                add_mapping_data(m)
                res.append(new_mapping_ins(id=vid, app_name=name,
                                           image_url=gen_url(bucket_name, file_name),
                                           fields=new_fields))
            final_time = time.time()
            logger.debug("[timing] prepare result costs: {:.3f}s".format(final_time - insert_time))

        return res
    except Exception as e:
        print(e)
        return e


def gen_url(bucket, name):
    return "http://{}/{}/{}".format(MINIO_ADDR, bucket, name)
