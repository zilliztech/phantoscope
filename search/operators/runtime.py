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

import docker


class DockerRuntime:
    def __init__(self, base_url, version, timeout, tls, user_agent, credstore_env):
        self.client = docker.DockerClient(base_url=base_url,
                                          version=version,
                                          timeout=timeout,
                                          tls=tls,
                                          user_agent=user_agent,
                                          credstore_env=credstore_env)

    def start_operator(self, name, image, ports, args=None):
        container = self.client.containers.run(image=image, name=name, detach=True, ports=ports)
        return container


def runtime_client_getter(name):
    if name == "docker":
        return DockerRuntime("unix://var/run/docker.sock", "1.35", 3, False, None, {})
