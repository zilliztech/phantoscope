import uuid
from application.application import application_detail
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NotExistError
from storage.storage import MilvusIns, S3Ins
from models.mapping import Mapping as DB
from models.mapping import add_mapping_data
from application.mapping import new_mapping_ins
from common.config import MINIO_ADDR
from common.utils import save_tmp_file


def upload(name, **kwargs):
    try:
        app = application_detail(name)
        if not app:
            raise NotExistError("application not exist", "application %s not exist" % name)
        bucket_name = app.buckets.split(",")[0]
        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "object"]
        pipeline_fields = {x: y['pipeline'] for x, y in app.fields.items() if y.get('type') == "object"}
        target_fields = kwargs['target_fields']
        if target_fields:
            target_file_name = "{}-{}-{}".format(name, "source", uuid.uuid4().hex)
            target_url = target_fields.get('url')
            target_data = target_fields.get("data")
            target_tmp_path = save_tmp_file(target_file_name, target_data, target_url)
            S3Ins.upload2bucket(bucket_name, target_tmp_path, target_file_name)

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
            S3Ins.upload2bucket(bucket_name, file_path, file_name)
            vectors = run_pipeline(pipe, data=file_data, url=url)
            milvus_collection_name = f"{pipe.name}_{pipe.encoder}"
            vids = MilvusIns.insert_vectors(milvus_collection_name, vectors)
            for vid in vids:
                m = DB(id=vid, app_name=name,
                       image_url=gen_url(bucket_name, file_name),
                       fields=new_fields,
                       target_fields=target_fields)
                add_mapping_data(m)
                res.append(new_mapping_ins(id=vid, app_name=name,
                                           image_url=gen_url(bucket_name, file_name),
                                           fields=new_fields,
                                           target_fields=target_fields))
        return res
    except Exception as e:
        return e


def gen_url(bucket, name):
    return "http://{}/{}/{}".format(MINIO_ADDR, bucket, name)
