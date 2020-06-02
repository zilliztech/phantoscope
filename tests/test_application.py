import os
import shutil
import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import PreOperator, PrePipeline


class TestApplicationApi:
    """test class for application api"""
    name = "pytestexample"
    field_name = 'image'
    op_name = "pytestop2"
    pipeline_name = "pytest_pipline2"
    test_url = 'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1906469856,4113625838&fm=26&gp=0.jpg'

    def test_list_application_api(self, client):
        rv = client.get("/v1/application/")
        assert rv.status_code == 200

    def test_application_detail_api_error(self, client):
        rv = client.get(f"/v1/application/{self.name}")
        assert rv.status_code != 200

    def test_new_application_api(self, client):
        PreOperator().create(
            {"endpoint": f"{local_ip()}:50001", "name": self.op_name})
        PrePipeline().create({
            "name": self.pipeline_name,
            "input": "image",
            "description": "this is a test pipeline",
            "processors": "",
            "encoder": self.op_name,
            "index_file_size": 1024
        })
        data = {
            'fields': {
                self.field_name: {
                    'type': 'object',
                    'pipeline': self.pipeline_name
                }
            },
            's3Buckets': "s3example"
        }
        rv = client.post(f'/v1/application/{self.name}', json=data)
        json_data = rv.get_json()
        assert rv.status_code == 200
        assert json_data['_application_name'] == self.name
        # os.mkdir('./tmp')

    def test_application_detail_api(self, client):
        rv = client.get(f"/v1/application/{self.name}")
        assert rv.status_code == 200

    def test_upload_api(self, client):
        data = {
            'fields': {
                self.field_name: {
                    'url': self.test_url
                }
            }
        }
        rv = client.post(f"/v1/application/{self.name}/upload", json=data)
        assert rv.status_code == 200

    def test_search_api(self, client):
        data = {
            'fields': {
                self.field_name: {
                    'url': self.test_url
                }
            },
            'topk': 5,
            'nprobe': 10
        }
        rv = client.post(f"/v1/application/{self.name}/search", json=data)
        assert rv.status_code == 200

    def test_entities_api(self, client):
        rv = client.get(f"/v1/application/{self.name}/entity")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']

    def test_delete_application_api(self, client):
        PrePipeline().delete({'name': self.pipeline_name})
        PreOperator().delete({'name': self.op_name})
        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code == 200
        # shutil.rmtree('./tmp', ignore_errors=True)

