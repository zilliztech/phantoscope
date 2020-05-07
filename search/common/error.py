class Error(Exception):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 503


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
    pass

class MilvusError(Error):
    pass

class S3Error(Error):
    pass


class DecodeError(Error):
    @property
    def error_code(self):
        return 400


class DownloadFileError(Error):
    @property
    def error_code(self):
        return 598


class PipelineIlegalError(Error):
    @property
    def error_code(self):
        return 400


class RPCExecError(Error):
    @property
    def error_code(self):
        return 503


class RequestError(Error):
    @property
    def error_code(self):
        return 400
