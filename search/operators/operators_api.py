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


from flask import Blueprint
from flask_restful import reqparse
from common.common import json_response
from operators.operator import all_operators
from operators.operator import regist_operators
from operators.operator import delete_operators
from operators.operator import operator_detail
from operators.operator import operator_health
from common.common import from_view_dict

operator = Blueprint('operator', __name__)


@operator.route("/")
@json_response
def operator_list_api():
    return all_operators()


@operator.route("/regist", methods=['POST'])
@json_response
def operator_refresh_api():
    args = reqparse.RequestParser(). \
         add_argument("endpoint", type=str, required=True). \
         add_argument("name", type=str, required=True). \
         parse_args()
    args = from_view_dict(args)
    ed = args['endpoint']
    name = args['name']
    return regist_operators(ed, name)


@operator.route("/<name>", methods=['DELETE'])
@json_response
def delete_operator_api(name):
    return delete_operators(name)


@operator.route("/<name>")
@json_response
def operator_detail_api(name):
    return operator_detail(name)


@operator.route("/<name>/health")
@json_response
def operator_health_api(name):
    return operator_health(name)
