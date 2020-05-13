import logging.config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask import Flask
from flask_cors import CORS
from common.config import UPLOAD_FOLDER
from common.config import META_DATABASE_ENDPOINT

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = META_DATABASE_ENDPOINT
if not database_exists(META_DATABASE_ENDPOINT):
    create_database(META_DATABASE_ENDPOINT)
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
CORS(app)


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
