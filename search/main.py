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

import argparse
from service import db
from models.pipeline import Pipeline
from models.application import Application
from models.mapping import Mapping
from models.operator import Operator
try:
    db.create_all()
except Exception as e:
    print(e)
from service.api import app


def app_runner(args):
    if args.debug:
        debug = True
    app.run(host="0.0.0.0", debug=debug, port=5000)


def run_with_args():
    parser = argparse.ArgumentParser(description='Start args')
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    app_runner(args)


if __name__ == "__main__":
    run_with_args()
