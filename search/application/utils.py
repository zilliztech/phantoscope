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
# Copyright (C) 2019-2020 Zilliz. All rights reserved.

from pipeline.pipeline import _all_pipelines


def pipeline_exist(name):
    all_pipelines_names = [x.name for x in _all_pipelines()]
    if name not in all_pipelines_names:
        return False
    return True


def fields_check(fields):
    check_list = {
        "pipeline": pipeline_exist,
        "string": lambda x : isinstance(x, str),
        "integer": lambda x: isinstance(x, int),
        "float": lambda x : isinstance(x, float)
    }

    if not isinstance(fields, dict):
        return False, "fields type error"
    for name, field in fields.items():
        if "type" not in field or "value" not in field:
            return False, f"type or value not in field {name}"
        if field.get("type") not in check_list:
            return False, f"type {field.get('type')} not in accept list"
        # get function from check list then do check
        if not check_list.get(field.get("type"))(field.get("value")):
            if field.get("type") == "pipeline":
                return False, f"pipeline {field.get('value')} not exist"
            return False, f"field {name} destination type {field.get('type')}, actual type {type(field.get('value'))}"
    return True, ""
