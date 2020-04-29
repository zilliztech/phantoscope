class Error(Exception):
    pass


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


class DownloadFileError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error


class PipelineIlegalError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error

class RPCExecError(Error):
    def __init__(self, message, error):
        self.message = message
        self.error = error
