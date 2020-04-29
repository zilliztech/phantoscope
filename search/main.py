import argparse
from service import db
from models.pipeline import Pipeline
from models.application import Application
from models.mapping import Mapping
from models.operator import Operator
from service.api import app


def create_tables_before_run():
    db.create_all()


def app_runner():
    app.run(host="0.0.0.0", debug=True, port=5000)


def run_with_args():
    create_tables_before_run()
    parser = argparse.ArgumentParser(description='Start args')
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    if args.debug:
        app_runner()


if __name__ == "__main__":
    run_with_args()
