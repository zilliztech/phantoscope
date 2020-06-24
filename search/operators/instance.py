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


class OperatorInstance:
    def __init__(self, id, name, status, ip, ports, endpoint=None):
        self.id = id
        self.name = name
        self.status = status
        self.ports = ports
        self.ip = ip
        self.endpoint = endpoint


def new_operator_instance(id, name, status, ip, ports):
    endpoint = f"{ip}:{ports['80/tcp'][0]['HostPort']}"
    endpoint = f"{ip}:80"
    return OperatorInstance(id, name, status, ip, ports, endpoint)
