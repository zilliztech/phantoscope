from test_basic import client
from utils.require import pre_operator, pre_instance
from utils.require import sleep_time


class TestPipelineApi:
    """test class for pipeline api"""
    name = "pytest_pipeline"

    @pre_operator(name="pytest1", type="encoder", addr="psoperator/vgg16-encoder:latest", version="0.1", description="")
    @pre_instance(operator_name="pytest1", name="ins1")
    @sleep_time(12)
    def test_create_pipeline_api(self, client):
        data = {
            "description": "this is a test pipeline",
            "processors": "",
            "encoder": {
                "name": "pytest1",
                "instance": "ins1"
            },
        }
        rv = client.post(f'/v1/pipeline/{self.name}', json=data)
        json_data = rv.get_json()
        assert rv.status_code == 200
        assert json_data['_pipeline_name'] == self.name

        # create exist pipeline
        rv = client.post(f'/v1/pipeline/{self.name}', json=data)
        assert rv.status_code != 200

        data = {
            "url": "https://live.staticflickr.com/65535/50063878058_c7c04603cc_o.jpg"
        }
        rv = client.post(f"/v1/pipeline/{self.name}/test", json=data)
        assert rv.status_code == 200

    def test_list_pipeline_api(self, client):
        rv = client.get("/v1/pipeline/")
        assert rv.status_code == 200

    def test_pipeline_detail_api(self, client):
        rv = client.get(f"/v1/pipeline/{self.name}")
        assert rv.status_code == 200
        # query none exist pipeline
        rv = client.get("/v1/pipeline/none_exist_pipeline")
        assert rv.status_code != 200

    def test_delete_pipeline_api(self, client):
        rv = client.delete(f"/v1/pipeline/{self.name}")
        assert rv.status_code == 200

    def test_pipeline_error_api(self, client):
        rv = client.delete(f"/v1/pipeline/{self.name}")
        assert rv.status_code != 200

        rv = client.post(f"/v1/pipeline/{self.name}/test")
        assert rv.status_code != 200
