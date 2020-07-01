import time
import pytest
from test_basic import client
from utils.require import sleep_time
from operators.client import health, identity, execute
from operators.instance import new_operator_instance


class TestOperatorApi:
    """test class for operator api"""
    name = "pytestop"
    addr = "psoperator/vgg16-encoder:latest"
    author = "tester"
    type = "encoder"
    description = "this is a test operator"
    version = "0.1"
    instance_name = "ins-test"

    def test_register_api(self, client):
        data = {
            "name": self.name,
            "addr": self.addr,
            "author": self.author,
            "type": self.type,
            "description": self.description,
            "version": self.version
        }
        rv = client.post('/v1/operator/register', json=data)
        json_data = rv.get_json()
        assert rv.status_code == 200
        assert json_data["_name"] == self.name
        assert json_data["_addr"] == self.addr

        # register exist operator
        rv = client.post('/v1/operator/register', json=data)
        assert rv.status_code != 200

    def test_fetch_operator(self, client):
        data = {
            "url": "http://23.99.118.156/v1/operator"
        }
        rv = client.post('/v1/operator/fetch', json=data)
        assert rv.status_code == 200

        data = {
            "url": "http://23.99.118.156/v1/operator",
            "override": False
        }
        rv = client.post('/v1/operator/fetch', json=data)
        assert rv.status_code == 200

        wrong_data = {
            "url": "http://1.1./v1/operator",
            "override": False
        }
        rv = client.post('/v1/operator/fetch', json=wrong_data)
        assert rv.status_code != 200

    def test_opreator_detail(self, client):
        rv = client.get(f"/v1/operator/{self.name}")
        assert rv.status_code == 200

    def test_operator_list(self, client):
        rv = client.get("/v1/operator/")
        assert rv.status_code == 200

    def test_create_instance(self, client):
        data = {
            "instanceName": self.instance_name
        }
        rv = client.post(f'/v1/operator/{self.name}/instances', json=data)
        assert rv.status_code == 200

    @sleep_time(5)
    def test_list_instacne(self, client):
        rv = client.get(f'/v1/operator/{self.name}/instances')
        assert len(rv.get_json()) == 1

    def test_stop_instance(self, client):
        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/stop')
        assert rv.status_code == 200

    def test_start_instance(self, client):
        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/start')
        assert rv.status_code == 200

    def test_restart_instance(self, client):
        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/restart')
        assert rv.status_code == 200

    def test_delete_instance(self, client):
        rv = client.delete(f'/v1/operator/{self.name}/instances/{self.instance_name}')
        assert rv.status_code == 200

    def test_instance_wrong(self, client):
        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/restart')
        assert rv.status_code != 200

        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/stop')
        assert rv.status_code != 200

        rv = client.post(f'/v1/operator/{self.name}/instances/{self.instance_name}/start')
        assert rv.status_code != 200

    def test_delete_operator(self, client):
        rv = client.delete(f"/v1/operator/{self.name}")
        assert rv.status_code == 200

    def test_error_operator(self, client):
        rv = client.get(f"/v1/operator/{self.name}")
        assert rv.status_code != 200

        rv = client.delete(f"/v1/operator/{self.name}")
        assert rv.status_code != 200

    def test_op_grpc_client(self):
        error_endpoint = '127.0.0.1:80'
        with pytest.raises(Exception):
            identity(error_endpoint)

        op = new_operator_instance(1, "name", "running", "127.0.0.1", "222")
        with pytest.raises(Exception):
            health(op)

        with pytest.raises(Exception):
            execute(op)
