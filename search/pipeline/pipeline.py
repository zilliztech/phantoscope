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
import json
from typing import List
from common.error import PipelineCheckError
from common.error import PipelineIllegalError
from common.error import RPCExecError
from common.error import NotExistError
from common.error import ExistError
from common.const import OPERATOR_TYPE_ENCODER
from common.const import OPERATOR_TYPE_PROCESSOR
from common.const import INSTANCE_STATUS_RUNNING
from operators.operator import all_operators
from operators.operator import operator_detail
from operators.client import execute, identity
from storage.storage import MilvusIns

logger = logging.getLogger(__name__)


class Pipeline():
    def __init__(self, name, input, output, description,
                 processors, encoder):
        self._pipeline_name = name
        self._input = input
        self._output = output
        self._pipeline_description = description
        self._processors = processors
        self._encoder = encoder
        self._description = description

    @property
    def name(self):
        return self._pipeline_name

    @property
    def description(self):
        return self._pipeline_description

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = input

    @property
    def output(self):
        return self.output

    @output.setter
    def output(self, output):
        self._output = output

    @property
    def processors(self):
        return self._processors

    @processors.setter
    def processors(self, processors):
        self._processors = processors

    @property
    def encoder(self):
        return self._encoder

    @encoder.setter
    def encoder(self, encoder):
        self._encoder = encoder

    def save(self):
        p = DB(name=self._pipeline_name, input=self._input,
               output=self._output, processors=json.dumps(self.processors),
               encoder=json.dumps(self.encoder), description=self._description)
        try:
            insert_pipeline(p)
        except Exception as e:
            raise e
        return self


def new_pipeline(name, input, output, description, processors, encoder):
    if isinstance(processors, str):
        processors = json.loads(processors)
    if isinstance(encoder, str):
        encoder = json.loads(encoder)
    return Pipeline(name=name, input=input, output=output,
                    description=description, processors=processors,
                    encoder=encoder)


def all_pipelines():
    res = []
    try:
        pipelines = search_pipeline()
        for p in pipelines:
            pipe = new_pipeline(name=p.Pipeline.name, input=p.Pipeline.input,
                                output=p.Pipeline.output,
                                description=p.Pipeline.description,
                                processors=p.Pipeline.processors,
                                encoder=p.Pipeline.encoder)
            res.append(pipe)
        return res
    except Exception as e:
        logger.error(e)
        raise e


def pipeline_detail(name):
    try:
        p = search_pipeline(name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        pipe = new_pipeline(name=p.name, input=p.input,
                            output=p.output,
                            description=p.description,
                            processors=p.processors,
                            encoder=p.encoder)
        return pipe
    except Exception as e:
        raise e


def create_pipeline(name, processors=None, encoder=None, description=None):
    try:
        p = search_pipeline(name)
        if p:
            raise ExistError(f"pipeline <{name}> already exists", "")
        pipe = new_pipeline(name=name, processors=processors, encoder=encoder,
                            description=description, input="", output="")
        if pipeline_illegal(pipe):
            raise PipelineIllegalError("Pipeline illegal check error", "")
        return pipe.save()
    except Exception as e:
        logger.error(e)
        raise e


def delete_pipeline(name):
    try:
        p = del_pipeline(name)
        if not p:
            raise NotExistError("pipeline %s is not exist" % name, "")
        p = p[0]
        pipe = new_pipeline(name=p.name, input=p.input,
                            output=p.output,
                            description=p.description,
                            processors=p.processors,
                            encoder=p.encoder)
        return pipe
    except Exception as e:
        logger.error(e)
        raise e


def run_pipeline(p, **kwargs):
    todo_list = []
    if not isinstance(p, Pipeline):
        raise PipelineCheckError("check pipeline with error", "%s is not a Pipeline" % p)
    for processor in p.processors:
        if not processor:
            continue
        op = operator_detail(processor["name"])
        ins = op.inspect_instance(processor["instance"])
        todo_list.append(ins)
    op = operator_detail(p.encoder["name"])
    ins = op.inspect_instance(p.encoder["instance"])
    todo_list.append(ins)

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
        pipe = search_pipeline(name)
        p = new_pipeline(name=pipe.name, input=pipe.input, output=pipe.output,
                         description=pipe.description, processors=pipe.processors,
                         encoder=pipe.encoder)
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
            op = operator_detail(operator.get("name"))
            # get container endpoint
            ins = op.inspect_instance(operator.get("instance"))
            if ins.status != INSTANCE_STATUS_RUNNING:
                raise PipelineIllegalError("Pipeline illegal check error", "")
            # use identity check container health
            info = identity(ins.endpoint)
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
    except Exception as e:
        raise e
