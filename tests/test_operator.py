import time
from test_basic import client


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
        print(json_data)
        assert json_data["_name"] == self.name
        assert json_data["_addr"] == self.addr

    def test_opreator_detail(self, client):
        rv = client.get(f"/v1/operator/{self.name}")
        assert rv.status_code == 200

    def test_operator_list(self, client):
        rv = client.get("/v1/operator/")
        assert rv.status_code == 200

    def test_create_instance(self, client):
        time.sleep(10)
        data = {
            "instanceName": self.instance_name
        }
        rv = client.post(f'/v1/operator/{self.name}/instances', json=data)
        assert rv.status_code == 200

    # @sleep_time(10)
    def test_list_instacne(self, client):
        rv = client.get(f'/v1/operator/{self.name}/instances')
        assert len(rv.get_json()) == 1

    def test_delete_instance(self, client):
        rv = client.delete(f'/v1/operator/{self.name}/instances/{self.instance_name}')
        assert rv.status_code == 200

    def test_delete_operator(self, client):
        rv = client.delete(f"/v1/operator/{self.name}")
        assert rv.status_code == 200
