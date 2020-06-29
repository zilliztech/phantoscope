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
from docker.errors import APIError
from common.error import DockerRuntimeError
from operators.instance import OperatorInstance
from operators.instance import new_operator_instance


class DockerRuntime:
    def __init__(self, base_url, version, timeout, tls, user_agent,
                 credstore_env):
        self.client = docker.DockerClient(base_url=base_url,
                                          version=version,
                                          timeout=timeout,
                                          tls=tls,
                                          user_agent=user_agent,
                                          credstore_env=credstore_env)
        self.labels = ["phantoscope"]

    def create_instance(self, name, image, ports, args=None):
        try:
            self.client.containers.run(image=image, name=name,
                                                   detach=True, ports=ports,
                                                   labels=self.labels)
            containers = self.client.containers.list(all=False, filters={"name": name})
            container = containers[0]
            return new_operator_instance(container.short_id, container.name,
                                         container.status, container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def start_instance(self, name):
        try:
            container = self.client.containers.get(name)
            container.start()
            return new_operator_instance(container.short_id, container.name,
                                         container.status, container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def stop_instance(self, name):
        try:
            container = self.client.containers.get(name)
            container.stop()
            return new_operator_instance(container.short_id, container.name,
                                         container.status, container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def delete_instance(self, name):
        try:
            container = self.client.containers.get(name)
            container.remove(force=True)
            return new_operator_instance(container.short_id, container.name,
                                         "deleted", container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def restart_instance(self, name):
        try:
            container = self.client.containers.get(name)
            container.restart()
            return new_operator_instance(container.short_id, container.name,
                                         container.status, container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def list_instances(self, name):
        try:
            res = []
            containers = self.client.containers.list(
                all=True, filters={"name": f"phantoscope_{name}", "label": self.labels})
            for container in containers:
                res.append(new_operator_instance(container.short_id,
                                                 container.name,
                                                 container.status,
                                                 container.attrs["NetworkSettings"]["IPAddress"],
                                                 container.ports))
            return res
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)

    def inspect_instance(self, name):
        try:
            container = self.client.containers.get(name)
            return new_operator_instance(container.short_id, container.name,
                                         container.status, container.attrs["NetworkSettings"]["IPAddress"],
                                         container.ports)
        except APIError as e:
            raise DockerRuntimeError(e.explanation, e)


def runtime_client_getter(name):
    if name == "docker":
        return DockerRuntime("unix://var/run/docker.sock", "1.35", 3, False, None, {})
