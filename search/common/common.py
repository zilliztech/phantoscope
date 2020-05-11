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
            if hasattr(res, "error_code"):
                res_code = res.error_code
            res = {
                "message": res.message,
                "error": res.error.__repr__()
            }
            res_body = json.dumps(res)
        elif isinstance(res, dict):
            res_body = json.dumps(res)
        else:
            res_body = json.dumps(res.__dict__)
        return Response(response=res_body, status=res_code, mimetype="application/json")
    return wrapper
