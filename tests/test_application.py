import os
import shutil
import time
import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import pre_instance, pre_operator, pre_pipeline, pre_application


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

    @pre_operator(name="pytest1", type="encoder", addr="psoperator/vgg16-encoder:latest", version="0.1", description="")
    @pre_instance(operator_name="pytest1", name="ins1")
    @pre_pipeline(name="test_pipeline", encoder={"name": "pytest1", "instance": "ins1"})
    def test_create_and_delete_application_api(self, client):
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

        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code == 200
        # delete none exist application
        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code != 200

    def test_new_application_api_error(self, client):
        # create wrong app
        none_exist_pipeline_data = {
            'fields': {
                self.field_name: {
                    'type': 'pipeline',
                    'value': 'none_exist_pipeline'
                }
            },
            's3Buckets': "s3example"
        }
        rv = client.post(f'/v1/application/{self.name}', json=none_exist_pipeline_data)
        assert rv.status_code != 200
        data = {
            'fields': {
                self.field_name: {
                    'type': 'str',
                    'value': self.pipeline_name
                }
            },
            's3Buckets': "s3example"
        }
        rv = client.post(f'/v1/application/{self.name}', json=data)
        assert rv.status_code != 200
        data = {
            'fields': {
                self.field_name: {
                    'type': 'pipeline',
                    'value': self.pipeline_name
                }
            },
            's3Buckets': "s3example"
        }
        rv = client.post(f'/v1/application/fail_app', json=data)
        assert rv.status_code != 200

    @pre_operator(name="pytest1", type="encoder", addr="psoperator/vgg16-encoder:latest", version="0.1", description="")
    @pre_instance(operator_name="pytest1", name="ins1")
    @pre_pipeline(name="test_pipeline", encoder={"name": "pytest1", "instance": "ins1"})
    @pre_application(name="pyapp1", fields={"full": {"type": "pipeline", "value": "pytest_pipe_1"}},
                     s3_buckets="s3example")
    def test_application_detail_api(self, client):
        rv = client.get("/v1/application/pyapp1")
        assert rv.status_code == 200

    @pre_operator(name="pytest1", type="encoder", addr="psoperator/vgg16-encoder:latest", version="0.1", description="")
    @pre_instance(operator_name="pytest1", name="ins1")
    @pre_pipeline(name="test_pipeline", encoder={"name": "pytest1", "instance": "ins1"})
    @pre_application(name="pyapp1", fields={"full": {"type": "pipeline", "value": "pytest_pipe_1"}},
                     s3_buckets="s3example")
    def test_application_other_api(self, client):
        data = {
            'fields': {
                self.field_name: {
                    'url': self.test_url
                }
            }
        }
        rv = client.post(f"/v1/application/{self.name}/upload", json=data)
        assert rv.status_code == 200
        base_txt = os.path.join(os.path.dirname(__file__), 'base64.txt')
        with open(base_txt, 'r')as file:
            base_data = file.readline()
            data = {
                'fields': {
                    self.field_name: {
                        'data': base_data
                    }
                }
            }
            rv = client.post(f"/v1/application/{self.name}/upload", json=data)
            assert rv.status_code == 200
        time.sleep(2)

        # search
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

        # search score function
        data = {
            'fields': {
                self.field_name: {
                    'url': self.test_url,
                    'inner_field_score_mode': 'first'
                }
            },
            'topk': 5,
            'nprobe': 10
        }
        rv = client.post(f"/v1/application/{self.name}/search", json=data)
        assert rv.status_code == 200

        # get all entities and delete all
        rv = client.get(f"/v1/application/{self.name}/entity")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']
        # delete none exist entity
        reply = client.delete(
            f"/v1/application/{self.name}/entity/-1")
        assert reply.status_code != 200


