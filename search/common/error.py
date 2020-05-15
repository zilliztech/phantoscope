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
