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
from common.error import InstanceExistError
from service import runtime_client


logger = logging.getLogger(__name__)


class Operator:
    def __init__(self, name, addr, author, version, type, description):
        self._name = name
        self._addr = addr
        self._author = author
        self._version = version
        self._type = type
        self._description = description

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def addr(self):
        return self._addr

    @property
    def author(self):
        return self._author

    @property
    def version(self):
        return self._version

    @property
    def dscription(self):
        return self._description


def new_operator(name, addr, author, version, type, description):
    return Operator(name=name, addr=addr, author=author, version=version,
                    type=type, description=description)

def all_operators():
    res = []
    try:
        operators = search_operator()
        for x in operators:
            res.append(new_operator(name=x.Operator.name,
                                    type=x.Operator.type,
                                    addr=x.Operator.addr,
                                    author=x.Operator.author,
                                    version=x.Operator.version,
                                    description=x.Operator.description))
    except Exception as e:
        logger.error(e)
        raise e
    return res


def delete_operators(name):
    try:
        op = del_operator(name)
        if not op:
            raise NotExistError("operator %s not exist" % name, "")
        return new_operator(name=op.name,
                            type=op.type,
                            addr=op.addr,
                            author=op.author,
                            version=op.version,
                            description=op.description)
    except Exception as e:
        logger.error(e)
        raise e


def operator_detail(name):
    try:
        op = search_operator(name)
        if not op:
            raise NotExistError("operator %s not exist" % name, "")
        return new_operator(name=op.name,
                            type=op.type,
                            addr=op.addr,
                            author=op.author,
                            version=op.version,
                            description=op.description)

    except Exception as e:
        logger.error(e)
        raise e

def regist_operators(name):
    pass

def create_operator_instance(name, ins_name):
    try:
        op = operator_detail(name)
        client = runtime_client
        ports = {"50001/tcp": None}
        container = client.start_operator(f"phantoscope_{name}_{ins_name}", op.addr, ports)
        return container.id
    except Exception as e:
        raise InstanceExistError(e.explanation, e)
