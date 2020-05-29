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


import ast


class Mapping:
    def __init__(self, id, app_name, image_url, fields):
        self._id = id
        self._app_name = app_name
        self._image_url = image_url
        self._fields = fields

def new_mapping_ins(id, app_name, image_url, fields):
    if isinstance(fields, str):
        fields = ast.literal_eval(fields)
    return Mapping(id=id, app_name=app_name, image_url=image_url,
                   fields=fields)
