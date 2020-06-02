from operators.operator import regist_operators, delete_operators
from pipeline.pipeline import new_pipeline, delete_pipeline
from application.application import new_application, delete_application


class PreResource:
    def create(self, data):
        pass

    def delete(self, data):
        pass


class PreOperator(PreResource):
    def create(self, data):
        regist_operators(data['endpoint'], data['name'])

    def delete(self, data):
        delete_operators(data['name'])


class PrePipeline(PreResource):
    def create(self, data):
        new_pipeline(data['name'], data['input'], data['index_file_size'],
                     data['processors'], data['encoder'], data['description'])

    def delete(self, data):
        delete_pipeline(data['name'])


class PreApplication(PreResource):
    def create(self, data):
        new_application(data['name'], data['fields'], data['s3_buckets'])

    def delete(self, data):
        delete_application(data['name'])
