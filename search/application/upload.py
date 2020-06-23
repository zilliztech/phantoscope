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


import uuid
import time
import logging
from application.application import application_detail
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NotExistError
from common.error import RequestError
from storage.storage import MilvusIns, S3Ins, MongoIns
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
        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "pipeline"]
        pipeline_fields = {x: y['value'] for x, y in app.fields.items() if y.get('type') == "pipeline"}
        new_fields = app.fields.copy()
        for k, v in kwargs.items():
            if k in accept_fields:
                new_fields[k]['value'] = v
        res = []
        for k, _ in kwargs.get('fields').items():
            if k not in accept_fields and k not in pipeline_fields:
                raise RequestError(f"fields {k} not in application", "")
        docs = {}
        for n, p in pipeline_fields.items():
            pipe = pipeline_detail(p)
            if not pipe:
                raise NotExistError("pipeline not exist", "pipeline %s not exist" % p)
            value = kwargs['fields'].get(n)
            file_data = value.get('data')
            url = value.get('url')
            if not file_data and not url:
                raise RequestError("can't find data or url from request", "")
            file_name = "{}-{}".format(name, uuid.uuid4().hex)
            file_path = save_tmp_file(file_name, file_data, url)

            S3Ins.upload2bucket(bucket_name, file_path, file_name)

            vectors = run_pipeline(pipe, data=file_data, url=url)

            milvus_collection_name = f"{app.name}_{pipe.encoder['name']}_{pipe.encoder['instance']}"
            vids = MilvusIns.insert_vectors(milvus_collection_name, vectors)
            docs[n] = {"ids": vids, "url": gen_url(bucket_name, file_name)}
            doc_id = MongoIns.insert_documents(f"{app.name}_entity", docs)
            res.append(new_mapping_ins(docs))
        return res
    except Exception as e:
        raise e


def gen_url(bucket, name):
    return "http://{}/{}/{}".format(MINIO_ADDR, bucket, name)
