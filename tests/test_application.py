import os
import time
import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import pre_instance
from utils.require import pre_operator
from utils.require import pre_pipeline
from utils.require import pre_application
from utils.require import sleep_time


class TestApplicationApi:
    """test class for application api"""
    test_ver = 2
    name = f"pytestexample{test_ver}"
    field_name = f"image{test_ver}"
    op_addr = "psoperator/vgg16-encoder:latest"
    op_type = "encoder"
    op_name = f"{test_ver}pytestop"
    op_instance = f"test_instance{test_ver}"
    pipeline_name = f"pytest_pipline{test_ver}"
    test_url = 'https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1906469856,4113625838&fm=26&gp=0.jpg'

    def test_list_application_api(self, client):
        rv = client.get("/v1/application/")
        assert rv.status_code == 200

    def test_application_detail_api_error(self, client):
        rv = client.get(f"/v1/application/{self.name}")
        assert rv.status_code != 200

    @pre_operator(name=op_name, type=op_type, addr=op_addr, version="0.1", description="")
    @sleep_time(10)  # wait for docker resource on github action
    @pre_instance(operator_name=op_name, name=op_instance)
    @pre_pipeline(name=pipeline_name,
                  encoder={"name": op_name, "instance": op_instance})
    @sleep_time(10)
    def test_create_and_delete_api(self, client):
        data = {
            'fields': {
                self.field_name: {
                    'type': 'pipeline',
                    'value': self.pipeline_name
                }
            },
            's3Buckets': f"s3example{self.test_ver}"
        }
        rv = client.post(f'/v1/application/{self.name}', json=data)
        json_data = rv.get_json()
        assert rv.status_code == 200
        assert json_data['_application_name'] == self.name

        rv = client.get(f"/v1/application/{self.name}")
        assert rv.status_code == 200

        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code == 200

        # delete none exist application
        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code != 200

    def test_new_application_api_error(self, client):
        """create wrong app"""
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
        # wrong_type_data = {
        #     'fields': {
        #         self.field_name: {
        #             'type': 'str',
        #             'value': self.pipeline_name
        #         }
        #     },
        #     's3Buckets': "s3example"
        # }
        # rv = client.post(f'/v1/application/{self.name}', json=wrong_type_data)
        # assert rv.status_code != 200

        # data = {
        #     'fields': {
        #         self.field_name: {
        #             'type': 'pipeline',
        #             'value': self.pipeline_name
        #         }
        #     },
        #     's3Buckets': "s3example"
        # }
        # rv = client.post(f'/v1/application/fail_app', json=data)
        # assert rv.status_code != 200

    @pre_operator(name=f"{op_name}1", type=op_type, addr=op_addr, version="0.1", description="")
    @pre_instance(operator_name=f"{op_name}1", name=f"{op_instance}1")
    @pre_pipeline(name=f"{pipeline_name}1",
                  encoder={"name": f"{op_name}1", "instance": f"{op_instance}1"})
    @pre_application(name=f"{name}1",
                     fields={field_name: {"type": "pipeline", "value": f"{pipeline_name}1"}},
                     s3_buckets=f"s3example{test_ver}")
    @sleep_time(12)  # sleep for opertaor instance initialization
    def test_application_other_api(self, client):
        # upload url image
        data = {
            'fields': {
                self.field_name: {
                    'url': self.test_url
                }
            }
        }
        rv = client.post(f"/v1/application/{self.name}1/upload", json=data)
        assert rv.status_code == 200

        # upload base64 image
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
            rv = client.post(f"/v1/application/{self.name}1/upload", json=data)
            assert rv.status_code == 200
        time.sleep(1)  # wait for milvus

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
        rv = client.post(f"/v1/application/{self.name}1/search", json=data)
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
        rv = client.post(f"/v1/application/{self.name}1/search", json=data)
        assert rv.status_code == 200

        # get all entities and delete all
        rv = client.get(f"/v1/application/{self.name}1/entity")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}1/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']
        # delete none exist entity
        reply = client.delete(
            f"/v1/application/{self.name}1/entity/-1")
        assert reply.status_code != 200
