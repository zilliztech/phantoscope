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
from operators.operator import register_operators
from operators.operator import delete_operators
from operators.operator import operator_detail
from operators.operator import fetch_operators
from common.common import from_view_dict

operator = Blueprint('operator', __name__)


@operator.route("/")
@json_response
def operator_list_api():
    return all_operators()


@operator.route("/register", methods=['POST'])
@json_response
def operator_refresh_api():
    args = reqparse.RequestParser(). \
        add_argument("name", type=str, required=True). \
        add_argument("addr", type=str, required=True). \
        add_argument("author", type=str, required=True). \
        add_argument("type", type=str, required=True). \
        add_argument("description", type=str, required=True). \
        add_argument("version", type=str, required=True). \
        parse_args()
    args = from_view_dict(args)
    return register_operators(**args)


@operator.route("/fetch", methods=['POST'])
@json_response
def operator_fetch_api():
    args = reqparse.RequestParser(). \
        add_argument("url", type=str, required=True). \
        add_argument("overwrite", type=bool, default=True). \
        parse_args()
    args = from_view_dict(args)
    url = args['url']
    overwrite = args['overwrite']
    return fetch_operators(url, overwrite)


@operator.route("/<name>", methods=['DELETE'])
@json_response
def delete_operator_api(name):
    return delete_operators(name)


@operator.route("/<name>")
@json_response
def operator_detail_api(name):
    return operator_detail(name)


@operator.route("/<name>/instances")
@json_response
def operator_instance_list_api(name):
    op = operator_detail(name)
    return op.list_instances()


@operator.route("/<name>/instances", methods=['POST'])
@json_response
def create_operator_instance_api(name):
    args = reqparse.RequestParser(). \
        add_argument("instanceName", type=str, required=True). \
        parse_args()
    args = from_view_dict(args)
    ins_name = args['instance_name']
    op = operator_detail(name)
    return op.new_instance(ins_name)


@operator.route("/<name>/instances/<ins_name>", methods=['DELETE'])
@json_response
def delete_operator_instance_api(name, ins_name):
    op = operator_detail(name)
    return op.delete_instance(ins_name)


@operator.route("/<name>/instances/<ins_name>/start", methods=['POST'])
@json_response
def start_operator_instance_api(name, ins_name):
    op = operator_detail(name)
    return op.start_instance(ins_name)


@operator.route("/<name>/instances/<ins_name>/stop", methods=['POST'])
@json_response
def stop_operator_instance_api(name, ins_name):
    op = operator_detail(name)
    return op.stop_instance(ins_name)


@operator.route("/<name>/instances/<ins_name>/restart", methods=['POST'])
@json_response
def restart_operator_instance_api(name, ins_name):
    op = operator_detail(name)
    return op.restart_instance(ins_name)
