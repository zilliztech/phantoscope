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
from common.common import from_view_dict, json_response
from pipeline.pipeline import all_pipelines
from pipeline.pipeline import pipeline_detail
from pipeline.pipeline import create_pipeline
from pipeline.pipeline import delete_pipeline
from pipeline.pipeline import test_pipeline


pipeline = Blueprint("pipeline", __name__)


@pipeline.route("/")
@json_response
def pipeline_list_api():
    return all_pipelines()


@pipeline.route("/<name>")
@json_response
def pipeline_detail_api(name):
    return pipeline_detail(name)


@pipeline.route("/<name>", methods=['POST'])
@json_response
def create_pipeline_api(name):
    args = reqparse.RequestParser(). \
        add_argument("description", type=str, required=True). \
        add_argument("processors", type=dict, required=True, action="append"). \
        add_argument("encoder", type=dict, required=True). \
        parse_args()
    args = from_view_dict(args)
    args['name'] = name
    return create_pipeline(**args)


@pipeline.route("/<name>/test", methods=['POST'])
@json_response
def pipeline_test_api(name):
    args = reqparse.RequestParser(). \
        add_argument("data", type=str). \
        add_argument("url", type=str). \
        parse_args()
    args = from_view_dict(args)
    return test_pipeline(name, args['data'], args['url'])


@pipeline.route("/<name>", methods=['DELETE'])
@json_response
def delete_pipeline_api(name):
    return delete_pipeline(name)
