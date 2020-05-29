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
from models.operator import Operator as DB
from models.operator import search_operator, insert_operator, del_operator
from operators.client import identity
from operators.client import health
from common.error import NotExistError
from common.error import OperatorRegistError


logger = logging.getLogger(__name__)


class Operator:
    def __init__(self, name, backend, type, input, output, endpoint="", dimension=0, metric_type=""):
        self._name = name
        self._backend = backend
        self._type = type
        self._input = input
        self._output = output
        self._endpoint = endpoint
        self._metric_type = metric_type
        self._dimension = dimension

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def metric_type(self):
        return self._metric_type

    @property
    def dimension(self):
        return self._dimension

    @property
    def output(self):
        return self._output

    @property
    def input(self):
        return self._input


def new_operator(name, backend, type, input, output, endpoint, dimension, metric_type):
    return Operator(name=name, backend=backend, type=type, input=input, output=output,
                    endpoint=endpoint, dimension=dimension, metric_type=metric_type)

def all_operators():
    res = []
    try:
        operators = search_operator()
        for x in operators:
            res.append(new_operator(name=x.Operator.name,
                                    backend=x.Operator.backend,
                                    type=x.Operator.type,
                                    input=x.Operator.input,
                                    output=x.Operator.output,
                                    endpoint=x.Operator.endpoint,
                                    dimension=x.Operator.dimension,
                                    metric_type=x.Operator.metric_type))
    except Exception as e:
        logger.error(e)
        return e
    return res


def regist_operators(endpoint, name):
    try:
        res = identity(endpoint)
        op = DB(name=name, backend=res['name'], type=res['type'], input=res['input'],
                output=res['output'], dimension=res['dimension'],
                metric_type=res['metric_type'], endpoint=res['endpoint'])
        insert_operator(op)
        logger.info("regist operator %s" % res['name'])
        return new_operator(name=op.name, backend=op.backend, type=op.type,
                            input=op.input,
                            output=op.output,
                            endpoint=op.endpoint,
                            dimension=op.dimension,
                            metric_type=op.metric_type)
    except Exception as e:
        logger.error(e)
        return OperatorRegistError("opeartor %s regist error" % name, e)


def delete_operators(name):
    try:
        op = del_operator(name)
        if not op:
            raise NotExistError("operator %s not exist" % name, "")
        return new_operator(name=op.name, backend=op.backend,
                            type=op.type,
                            input=op.input,
                            output=op.output,
                            endpoint=op.endpoint,
                            dimension=op.dimension,
                            metric_type=op.metric_type)
    except Exception as e:
        logger.error(e)
        return e


def operator_detail(name):
    try:
        op = search_operator(name)
        if not op:
            raise NotExistError("operator %s not exist" % name, "")
        return new_operator(name=op.name, backend=op.backend,
                            type=op.type,
                            input=op.input,
                            output=op.output,
                            endpoint=op.endpoint,
                            dimension=op.dimension,
                            metric_type=op.metric_type)
    except Exception as e:
        logger.error(e)
        raise e

def operator_health(name):
    try:
        op = search_operator(name)
        if not op:
            raise NotExistError("operator %s not exist" % name, "")
        return health(op)
    except Exception as e:
        logger.error(e)
        return e
