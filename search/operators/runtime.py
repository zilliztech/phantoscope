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
from operators.instance import OperatorInstance
from operators.instance import new_operator_instance


class DockerRuntime:
    def __init__(self, base_url, version, timeout, tls, user_agent, credstore_env):
        self.client = docker.DockerClient(base_url=base_url,
                                          version=version,
                                          timeout=timeout,
                                          tls=tls,
                                          user_agent=user_agent,
                                          credstore_env=credstore_env)

    def create_instance(self, name, image, ports, args=None):
        container = self.client.containers.run(image=image, name=name, detach=True, ports=ports)
        return new_operator_instance(container.short_id, container.name, container.status, container.ports)

    def start_instance(self, name):
        container = self.client.container.get(name)
        container.start()
        return new_operator_instance(container.short_id, container.name, container.status, container.ports)

    def stop_instance(self, name):
        container = self.client.containers.get(name)
        container.stop()
        return new_operator_instance(container.short_id, container.name, container.status, container.ports)

    def delete_instance(self, name):
        try:
            container = self.client.containers.get(name)
            container.remove(force=True)
            return new_operator_instance(container.short_id, container.name, "deleted", container.ports)
        except Exception as e:
            print(e)

    def restart_instance(self, name):
        container = self.client.containers.get(name)
        container.restart()
        return new_operator_instance(container.short_id, container.name, container.status, container.ports)

    def list_instances(self, name):
        try:
            res = []
            containers = self.client.containers.list(all=True, filters={"name": f"phantoscope_{name}"})
            for container in containers:
                res.append(new_operator_instance(container.short_id, container.name, container.status, container.ports))
            return res
        except Exception as e:
            print(e)


def runtime_client_getter(name):
    if name == "docker":
        return DockerRuntime("unix://var/run/docker.sock", "1.35", 3, False, None, {})
