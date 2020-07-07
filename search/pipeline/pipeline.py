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
from common.error import PipelineCheckError
from common.error import PipelineIllegalError
from common.error import RPCExecError
from common.error import NotExistError
from common.error import ExistError
from common.const import OPERATOR_TYPE_ENCODER
from common.const import OPERATOR_TYPE_PROCESSOR
from common.const import PIPELINE_COLLECTION_NAME
from operators.operator import operator_detail
from operators.client import execute, identity
from storage.storage import MongoIns

logger = logging.getLogger(__name__)


class Pipeline(Resource):
    def __init__(self, name, description,
                 processors, encoder, input=None, output=None):
        self.name = name
        self.input = input
        self.output = output
        self.processors = processors
        self.encoder = encoder
        self.description = description
        self.metadata = None


def all_pipelines():
    res = []
    try:
        pipes = MongoIns.list_documents(PIPELINE_COLLECTION_NAME, 0)
        for pipe in pipes:
            p = Pipeline(pipe["name"], pipe["description"], pipe["processors"],
                         pipe["encoder"], pipe["input"], pipe["output"])
            p.metadata = pipe["metadata"]
            res.append(p)
        return res
    except Exception as e:
        logger.error(e)
        raise e


def pipeline_detail(name):
    try:
        p = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        p = p[0]
        pipe = Pipeline(p["name"], p["description"], p["processors"], p["encoder"], p["input"], p["output"])
        pipe.metadata = p["metadata"]
        return pipe
    except Exception as e:
        raise e


def create_pipeline(name, processors=None, encoder=None, description=None):
    try:
        p = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, name)
        if p:
            raise ExistError(f"pipeline <{name}> already exists", "")
        pro = []
        encoder_res = {}
        for processor in processors:
            pro.append(operator_detail(processor["name"]))
        e = operator_detail(encoder["name"])
        encoder_res["operator"] = e.to_dict()
        encoder_res["instance"] = e.inspect_instance(encoder["instance"])
        pipe = Pipeline(name, description, pro, encoder_res)
        pipe.metadata = pipe._metadata()
        if pipeline_illegal(pipe):
            raise PipelineIllegalError("Pipeline illegal check error", "")
        MongoIns.insert_documents(PIPELINE_COLLECTION_NAME, pipe.to_dict())
        return pipe
    except Exception as e:
        logger.error(e)
        raise e


def delete_pipeline(name):
    try:
        p = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        p = p[0]
        MongoIns.delete_by_name(PIPELINE_COLLECTION_NAME, name)
        pipe = Pipeline(p["name"], p["description"], p["processors"], p["encoder"], p["input"], p["output"])
        pipe.metadata = p["metadata"]
        return pipe
    except Exception as e:
        logger.error(e)
        raise e


def run_pipeline(p, **kwargs):
    todo_list = []
    if not isinstance(p, Pipeline):
        raise PipelineCheckError("check pipeline with error", "%s is not a Pipeline" % p)
    for processor in p.processors:
        todo_list.append(processor["instance"])
    todo_list.append(p.encoder["instance"])

    def runner(todo_list):
        metadata, vectors = [], []
        urls = [kwargs['url']] if kwargs['url'] else []
        datas = [kwargs['data']] if kwargs['data'] else []
        try:
            for num, i in enumerate(todo_list):
                if num == len(todo_list) - 1:
                    vectors, _ = execute(i, urls=urls, datas=datas)
                    return vectors
                _, metadatas = execute(i, urls=urls, datas=datas)
                urls = [x.url for x in metadatas]
                datas = [x.data for x in metadatas]
            return metadata
        except Exception as e:
            raise RPCExecError("Execute with error", e)

    try:
        return runner(todo_list)
    except Exception as e:
        logger.error(e)
        raise e


def test_pipeline(name, data=None, url=None):
    try:
        pipe = MongoIns.search_by_name(PIPELINE_COLLECTION_NAME, name)
        if not pipe:
            raise NotExistError("pipeline %s is not exist" % name, "")
        pipe = pipe[0]
        p = Pipeline(pipe["name"], pipe["description"], pipe["processors"],
                     pipe["encoder"], pipe["input"], pipe["output"])
        p.metadata = pipe["metadata"]
        return {"result": run_pipeline(p, data=data, url=url)}
    except Exception as e:
        raise e


def pipeline_illegal(pipe):
    input, output = None, None
    try:
        operators = pipe.processors.copy()
        operators.append(pipe.encoder)
        for num, operator in enumerate(operators):
            # check operator and instance exist
            # use identity check container health
            info = identity(operator['instance'].endpoint)
            if num == len(operators)-1:
                if info.get("type") != OPERATOR_TYPE_ENCODER:
                    raise PipelineIllegalError("Pipeline illegal check error", "")
            else:
                if info.get("type") != OPERATOR_TYPE_PROCESSOR:
                    raise PipelineIllegalError("Pipeline illegal check error", "")
            # check input and output
            if not input and not output:
                input, output = info.get("input"), info.get("output")
            else:
                if output != info.get("input"):
                    raise PipelineIllegalError("Pipeline illegal check error", "")
            pipe.input, pipe.output = input, output
    except Exception as e:
        raise e
