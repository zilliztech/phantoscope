# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.


from flask import Blueprint
from flask_restful import reqparse
from common.common import from_view_dict, json_response
from application.application import new_application
from application.application import all_applications
from application.application import application_detail
from application.application import delete_application
from application.application import entities_list
from application.application import delete_entity
from application.application import count_entities
from application.upload import upload
from application.search import search

application = Blueprint("application", __name__)


@application.route("/")
@json_response
def application_list_api():
    return all_applications()


@application.route("/<name>")
@json_response
def application_detail_api(name):
    return application_detail(name)


@application.route("/<name>", methods=['POST'])
@json_response
def new_application_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        add_argument("s3Buckets", type=str, required=True). \
        parse_args()
    args = from_view_dict(args)
    args['app_name'] = name
    return new_application(**args)


@application.route("/<name>", methods=['DELETE'])
@json_response
def delete_application_api(name):
    return delete_application(name)


@application.route("/<name>/search", methods=['POST'])
@json_response
def application_do_search_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        add_argument("topk", type=int, required=True). \
        add_argument("nprobe", type=int, required=False, default=16). \
        parse_args()
    args = from_view_dict(args)
    return search(name,
                  fields=args['fields'],
                  topk=args['topk'],
                  nprobe=args['nprobe'])


@application.route("/<name>/upload", methods=["POST"])
@json_response
def application_do_upload_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        parse_args()
    args = from_view_dict(args)
    return upload(name, **args)


@application.route("/<app_name>/entity")
@json_response
def entities_list_api(app_name):
    args = reqparse.RequestParser(). \
        add_argument("num", type=int, default=10). \
        add_argument("page", type=int, default=0). \
        parse_args()
    args = from_view_dict(args)
    num = args['num']
    page = args['page']
    return entities_list(app_name, num, page)


@application.route("/<app_name>/entity/count")
@json_response
def count_entities_api(app_name):
    return count_entities(app_name)


@application.route("/<app_name>/entity/<entity_name>", methods=["DELETE"])
@json_response
def delete_entity_api(app_name, entity_name):
    return delete_entity(app_name, entity_name)
