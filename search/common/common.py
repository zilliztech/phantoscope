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
from functools import wraps
from inflection import underscore
from flask import jsonify
from flask import Response
from common.config import ALLOWED_EXTENSIONS
from common.config import LOCAL_CACHE_PATH


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def from_view_dict(values):
    return {underscore(k): v for k, v in values.items()}


def format_response(values):
    if isinstance(values, dict):
        return jsonify(values)
    return jsonify(values.__dict__)


def json_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            res = e
        res_code = 200
        if isinstance(res, list):
            res_body = json.dumps([r.__dict__ for r in res])
        elif isinstance(res, str):
            res_body = res
        elif isinstance(res, tuple):
            res_body, res_code = res
            if isinstance(res_body, list):
                res_body = json.dumps([r.__dict__ for r in res_body])
        elif isinstance(res, Exception):
            res_code = 500
            res_body = {
                "message": "",
                "error": ""
            }
            if hasattr(res, "code"):
                res_code = res.code
            if hasattr(res, "description"):
                res_body["message"] = res.description
            if hasattr(res, "name"):
                res_body["error"] = res.name
            res_body = json.dumps(res_body)
        elif isinstance(res, dict):
            res_body = json.dumps(res)
        else:
            res_body = json.dumps(res.__dict__)
        return Response(response=res_body, status=res_code, mimetype="application/json")
    return wrapper
