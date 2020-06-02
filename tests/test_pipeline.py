import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import PreOperator


def test_get_pipeline(client):
    rv = client.get("/v1/pipeline/")
    assert rv.status_code == 200


class TestPipelineApi:
    """test class for pipeline api"""
    name = "pytest_pipeline"

    def test_create_pipeline_api(self, client):
        PreOperator().create({"endpoint": f"{local_ip()}:50001", "name": "pytestop"})
        data = {
            "input": "image",
            "description": "this is a test pipeline",
            "processors": "",
            "encoder": "pytestop",
            "indexFileSize": 1024
        }
        rv = client.post(f'/v1/pipeline/{self.name}', json=data)
        json_data = rv.get_json()
        PreOperator().delete({"name": "pytestop"})
        assert rv.status_code == 200
        assert json_data['_pipeline_name'] == self.name

    def test_list_pipeline_api(self, client):
        rv = client.get("/v1/pipeline/")
        assert rv.status_code == 200

    def test_pipeline_detail_api(self, client):
        rv = client.get(f"/v1/pipeline/{self.name}")
        assert rv.status_code == 200
        # query none exist pipeline
        rv = client.get(f"/v1/pipeline/none_exist_pipeline")
        assert rv.status_code != 200

    def test_delete_pipeline_api(self,client):
        rv = client.delete(f"/v1/pipeline/{self.name}")
        assert rv.status_code == 200
