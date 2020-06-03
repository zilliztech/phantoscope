import pytest
from test_basic import client
from test_basic import local_ip
from operators.operator import new_operator
from operators.operator import Operator


class TestOperatorApi:
    """test class for operator api"""
    name = "pytestop"
    endpoint = f"{local_ip()}:50001"

    def test_regist_api(self, client):
        data = {"endpoint": self.endpoint, "name": self.name}
        rv = client.post('/v1/operator/regist', json=data)
        json_data = rv.get_json()
        assert json_data["_endpoint"] == self.endpoint
        assert json_data["_name"] == self.name

    def test_opreator_detail(self, client):
        rv = client.get(f"/v1/operator/{self.name}")
        assert rv.status_code == 200

    def test_operator_list(self, client):
        rv = client.get("/v1/operator/")
        assert rv.status_code == 200

    def test_operator_health(self, client):
        rv = client.get(f"/v1/operator/{self.name}/health")
        assert rv.status_code == 200

    def test_delete_operator(self, client):
        rv = client.delete(f"/v1/operator/{self.name}")
        assert rv.status_code == 200
