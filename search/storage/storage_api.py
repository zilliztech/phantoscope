from flask import Blueprint

storage = Blueprint("storage", __name__)


@storage.route("/")
def storage_list_api():
    return ""
