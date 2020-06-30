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


class Error(Exception):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def code(self):
        return 503

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def description(self):
        return self.message


class OperatorImportError(Error):
    pass


class OperatorRegistError(Error):
    pass


class PipelineCheckError(Error):
    pass


class Insert2SQLError(Error):
    pass


class QueryFromSQLError(Error):
    pass


class DeleteFromSQLError(Error):
    pass


class UpdateFromSQLError(Error):
    pass


class ExistError(Error):
    @property
    def code(self):
        return 400


class NotExistError(Error):
    @property
    def code(self):
        return 404


class MilvusError(Error):
    pass


class S3Error(Error):
    pass


class DecodeError(Error):
    @property
    def code(self):
        return 400


class DownloadFileError(Error):
    @property
    def code(self):
        return 598


class PipelineIlegalError(Error):
    @property
    def code(self):
        return 400


class RPCExecError(Error):
    @property
    def code(self):
        return 503


class RequestError(Error):
    @property
    def code(self):
        return 400


class NoneVectorError(Error):
    @property
    def code(self):
        return 400


class InstanceExistError(Error):
    @property
    def code(self):
        return 409


class DockerRuntimeError(Error):
    @property
    def code(self):
        return 400


class WrongFieldModeError(Error):
    @property
    def code(self):
        return 400


class WrongInnerFieldModeError(Error):
    @property
    def code(self):
        return 400


class ArgsCheckError(Error):
    @property
    def code(self):
        return 400


class NoneValidFieldError(Error):
    @property
    def code(self):
        return 400


class UnexpectedError(Error):
    @property
    def code(self):
        return 400
