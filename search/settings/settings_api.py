from flask import Blueprint
from common.common import json_response


settings = Blueprint("settings", __name__)


@settings.route("/ping")
@json_response
def settings_ping():
    return "pong"
