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


from application.application import application_detail
from application.mapping import new_mapping_ins
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NoneVectorError
from common.error import RequestError
from storage.storage import MilvusIns


def search(name, fields={}, topk=10, nprobe=16):
    res = []
    try:
        app = application_detail(name)
        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "pipeline"]
        pipeline_fields = {x: y['value'] for x, y in app.fields.items() if y.get('type') == "pipeline"}
        for k, _ in fields.items():
            if k not in accept_fields and k not in pipeline_fields:
                raise RequestError(f"fields {k} not in application", "")
        for n, p in pipeline_fields.items():
            pipe = pipeline_detail(p)
            value = fields.get(n)
            file_data = value.get('data')
            url = value.get('url')
            if not file_data and not url:
                raise RequestError("can't find data or url from request", "")
            vectors = run_pipeline(pipe, data=file_data, url=url)
            if not vectors:
                raise NoneVectorError("can't encode data by encoder, check input or encoder", "")

        return res
    except Exception as e:
        raise e
