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
import json
import uuid
from collections import namedtuple
import time
import datetime
from resource.resource import Resource, new_resource
import logging
import requests
from storage.storage import MongoIns
from operators.client import identity
from operators.client import health
from common.error import NotExistError
from common.error import OperatorRegistError
from common.error import InstanceExistError
from common.error import ExistError
from common.error import DockerRuntimeError
from common.error import RequestError
from common.config import DEFAULT_RUNTIME
from common.const import MARKET_IDENTITY_HEADER
from common.const import OPERATOR_COLLECTION_NAME
from service import runtime_client
from operators.instance import OperatorInstance

logger = logging.getLogger(__name__)


class Operator(Resource):
    def __init__(self, name, addr, author, version, type, description):
        self.name = name
        self.addr = addr
        self.author = author
        self.version = version
        self.type = type
        self.description = description
        self.runtime_client = DEFAULT_RUNTIME
        self.metadata = None

    @property
    def runtime(self):
        self.runtime_client = runtime_client
        return self.runtime_client

    def list_instances(self):
        return self.runtime.list_instances(self.name)

    def new_instance(self, name):
        ports = {"80/tcp": None}
        ins = self.runtime.create_instance(f"phantoscope_{self.name}_{name}", self.addr, ports)
        return ins

    def delete_instance(self, name):
        try:
            ins = self.runtime.delete_instance(f"phantoscope_{self.name}_{name}")
            return ins
        except DockerRuntimeError as e:
            raise e

    def stop_instance(self, name):
        ins = self.runtime.stop_instance(f"phantoscope_{self.name}_{name}")
        return ins

    def start_instance(self, name):
        ins = self.runtime.start_instance(f"phantoscope_{self.name}_{name}")
        return ins

    def restart_instance(self, name):
        ins = self.runtime.restart_instance(f"phantoscope_{self.name}_{name}")
        return ins

    def inspect_instance(self, name):
        ins = self.runtime.inspect_instance(f"phantoscope_{self.name}_{name}")
        return ins


def all_operators():
    res = []
    try:
        operators = MongoIns.list_documents(OPERATOR_COLLECTION_NAME, 0)
        for x in operators:
            op = Operator(x["name"], x["addr"], x["author"], x["version"], x["type"], x["description"])
            op.metadata = x["metadata"]
            res.append(op)
        return res
    except Exception as e:
        logger.error(e)
        raise e


def delete_operators(name):
    try:
        op = MongoIns.search_by_name(OPERATOR_COLLECTION_NAME, name)
        if not op:
            raise NotExistError(f"operator {name} not exist", "")
        op = op[0]
        MongoIns.delete_by_name(OPERATOR_COLLECTION_NAME, name)
        operator = Operator(op["name"], op["addr"], op["author"], op["version"], op["type"], op["description"])
        operator.metadata = op["metadata"]
        return operator
    except Exception as e:
        logger.error(e)
        raise e


def operator_detail(name):
    try:
        op = MongoIns.search_by_name(OPERATOR_COLLECTION_NAME, name)
        if not op:
            raise NotExistError(f"operator {name} not exist", "")
        op = op[0]
        operator = Operator(op["name"], op["addr"], op["author"], op["version"], op["type"], op["description"])
        operator.metadata = op["metadata"]
        return operator
    except Exception as e:
        logger.error(e)
        raise e


def register_operators(name, addr, author, version, type, description):
    try:
        op = Operator(name, addr, author, version, type, description)
        op.metadata = op._metadata()
        if MongoIns.search_by_name(OPERATOR_COLLECTION_NAME, name):
            raise ExistError(f"operator {name} had exist", "")
        MongoIns.insert_documents(OPERATOR_COLLECTION_NAME, op.to_dict())
        return op.to_dict()
    except Exception as e:
        logger.error(f"Unexpected error happen during register operator, {str(e)}", exc_info=True)
        raise e


def fetch_operators(url, overwrite=True):
    """fetch operators from origin market

    url -- origin url
    overwrite -- Whether to overwrite local information if the same name exists

    """
    origin = []
    try:
        r = requests.get(url)
        if r.headers.get(MARKET_IDENTITY_HEADER) != "0.1.0":
            raise RequestError("Uncertified market", "")
        if r.status_code != 200:
            raise RequestError(r.text, r.status_code)
    except Exception as e:
        raise RequestError(e.args[0], e)
    for op in r.json():
        origin.append(Operator(op['name'], op['addr'], op['author'],
                               op['version'], op['type'], op['description']))
    local_operators = all_operators()
    local_operator_names = [x.name for x in local_operators]
    for x in origin:
        if x.name not in local_operator_names:
            local_operators.append(x)
        else:
            if overwrite:
                for lop in local_operators:
                    if lop.name == x.name:
                        local_operators.remove(lop)
                        local_operators.append(x)
    MongoIns.delete_mongo_collection(OPERATOR_COLLECTION_NAME)
    for x in local_operators:
        MongoIns.insert_documents(OPERATOR_COLLECTION_NAME, x.to_dict())
    return local_operators
