import os
import shutil
import time
import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import PreOperator, PrePipeline


class TestScoreFunctionApi:
    """test class for application api"""
    name = "pytestexample3"
    field_name1 = 'detector'
    field_name2 = 'none-detector'
    detector_name = "pytest_ssd"
    encoder_name = "pytest_vgg"
    pipeline_name1 = "pytest_pipline3"
    pipeline_name2 = "pytest_pipline4"
    inner_fields = ['first', 'random', 'avg', 'distance_first']
    test_url = ['https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1906469856,4113625838&fm=26&gp=0.jpg',
                'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592371648552&di=28d2be13f40539aacaa81ab5f43642e6&imgtype=0&src=http%3A%2F%2Fphotocdn.sohu.com%2F20151130%2Fmp45332712_1448864892504_4.jpeg',
                'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592375248588&di=13521ac5965776e504dde2e242610293&imgtype=0&src=http%3A%2F%2Ft8.baidu.com%2Fit%2Fu%3D2388511970%2C557698405%26fm%3D193',
                'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1668363641,4252982095&fm=26&gp=0.jpg']

    test_search_url = ['https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=3442599741,2386083112&fm=26&gp=0.jpg',
                       'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1389311444,3919902992&fm=26&gp=0.jpg']

    def test_new_application_api(self, client):
        PreOperator().create(
            {"endpoint": f"{local_ip()}:50010", "name": self.detector_name})
        PreOperator().create(
            {"endpoint": f"{local_ip()}:50001", "name": self.encoder_name})
        PrePipeline().create({
            "name": self.pipeline_name1,
            "input": "image",
            "description": "this is a detector test pipeline",
            "processors": self.detector_name,
            "encoder": self.encoder_name,
            "index_file_size": 1024
        })
        PrePipeline().create({
            "name": self.pipeline_name2,
            "input": "image",
            "description": "this is a test pipeline",
            "processors": "",
            "encoder": self.encoder_name,
            "index_file_size": 1024
        })
        data = {
            'fields': {
                self.field_name1: {
                    'type': 'object',
                    'pipeline': self.pipeline_name1
                },
                self.field_name2: {
                    'type': 'object',
                    'pipeline': self.pipeline_name2
                }
            },
            's3Buckets': "s3example334"
        }
        rv = client.post(f'/v1/application/{self.name}', json=data)
        json_data = rv.get_json()
        assert rv.status_code == 200
        assert json_data['_application_name'] == self.name

    def test_upload_api(self, client):
        for image_url in self.test_url:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': image_url
                    }
                }
            }
            rv = client.post(f"/v1/application/{self.name}/upload", json=data)
            assert rv.status_code == 200
        time.sleep(1)

    def test_score_function_inner(self, client):
        for inner_field_score_mode in self.inner_fields:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': self.test_search_url[0],
                        'inner_field_score_mode': inner_field_score_mode
                    }
                },
                'topk': 3,
                'nprobe': 10
            }
            rv = client.post(f"/v1/application/{self.name}/search", json=data)
            assert rv.status_code == 200
            json_data = rv.get_json()
            assert len(json_data) == 3

    def test_score_function_insufficent_topk(self, client):
        topk = len(self.test_url) * 10
        for inner_field_score_mode in self.inner_fields:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': self.test_search_url[0],
                        'inner_field_score_mode': inner_field_score_mode
                    }
                },
                'topk': topk,
                'nprobe': 10
            }
            rv = client.post(f"/v1/application/{self.name}/search", json=data)
            assert rv.status_code == 200
            json_data = rv.get_json()
            assert len(json_data) > 0
            assert len(json_data) < topk

    def test_multi_field_score_function(self, client):
        topk = len(self.test_url) * 10
        for inner_field_score_mode in self.inner_fields:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': self.test_search_url[0],
                        'inner_field_score_mode': inner_field_score_mode,
                        'weight': 6
                    },
                    self.field_name2: {
                        'url': self.test_search_url[1],
                        'inner_field_score_mode': inner_field_score_mode,
                        'weight': 2
                    }
                },
                'topk': topk,
                'nprobe': 10
            }
            pass

    def test_entities_api(self, client):
        rv = client.get(f"/v1/application/{self.name}/entity?num=100")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']

    def test_delete_application_api(self, client):
        PrePipeline().delete({'name': self.pipeline_name1})
        PrePipeline().delete({'name': self.pipeline_name2})
        PreOperator().delete({'name': self.detector_name})
        PreOperator().delete({'name': self.encoder_name})
        rv = client.delete(f"/v1/application/{self.name}")
        assert rv.status_code == 200
