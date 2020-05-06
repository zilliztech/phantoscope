class Error(Exception):
    @property
    def error_code(self):
        return 503


class OperatorImportError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class PipelineCheckError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class Insert2SQLError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class QueryFromSQLError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class DeleteFromSQLError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class UpdateFromSQLError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class NotExistError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class MilvusError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class S3Error(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class DecodeError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 400


class DownloadFileError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 598


class PipelineIlegalError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 400


class RPCExecError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 503

class RequestError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    @property
    def error_code(self):
        return 400
