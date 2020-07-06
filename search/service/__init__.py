import logging.config
from flask import Flask
from flask_cors import CORS
from common.config import UPLOAD_FOLDER
from common.config import DEFAULT_RUNTIME
from common.config import MONGO_METADATA_COLLECTIONS
from operators.runtime import runtime_client_getter
from storage.storage import MongoIns

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

for collection in MONGO_METADATA_COLLECTIONS:
    if not MongoIns.collection_exists(collection):
        MongoIns.new_mongo_collection(collection)

CORS(app)

runtime_client = runtime_client_getter(DEFAULT_RUNTIME)

logger_dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": '[%(asctime)s] %(levelname)s in %(name)s %(lineno)d: %(message)s'
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "default",
            "filename": "errors.log",
            "encoding": "utf8"
        },
        "access_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "access.log",
            "encoding": "utf8"
        }
    },
    # "loggers": {
    #     "werkzeug": {
    #         "level": "DEBUG",
    #         "handlers": ["wsgi"],
    #         "propagate": "no"
    #     }
    # }
    "root": {
        "level": "INFO",
        "handlers": ["wsgi", "error_file_handler", "access_file_handler"]
    }
}

logging.config.dictConfig(logger_dict_config)
