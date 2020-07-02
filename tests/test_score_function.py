import time
from test_basic import client
from utils.require import pre_instance
from utils.require import pre_operator
from utils.require import pre_pipeline
from utils.require import pre_application
from utils.require import sleep_time


class TestScoreFunctionApi:
    """test class for application api"""
    test_ver = 2
    name = f"pytestexample{test_ver}"
    field_name1 = f'detector{test_ver}'
    field_name2 = f'none-detector{test_ver}'
    encoder_addr = "psoperator/vgg16-encoder:latest"
    encoder_type = "encoder"
    encoder_name = f"pytestop{test_ver}"
    encoder_instance = f"test_instance{test_ver}"
    encoder_instance2 = f"test_instance2{test_ver}"

    detector_addr = "psoperator/ssd-detector:latest"
    detector_type = "processor"
    detector_name = f"pytestop2{test_ver}"
    detector_instance = f"test_instance3{test_ver}"

    pipeline_name1 = f"pytest_pipline3{test_ver}"
    pipeline_name2 = f"pytest_pipline4{test_ver}"

    inner_fields = ['first', 'random', 'avg', 'distance_first']
    score_modes = ['first', 'sum', 'max', 'min', 'multiple', 'avg']
    test_url = ['https://live.staticflickr.com/65535/50064435471_0583cf876c_o.jpg',
                'https://live.staticflickr.com/65535/50063878058_c7c04603cc_o.jpg',
                'https://live.staticflickr.com/65535/50064692802_90aed5e68a_o.jpg',
                'https://live.staticflickr.com/65535/50064709412_e204654f9b_o.jpg']

    test_search_url = ['https://live.staticflickr.com/65535/50064411181_574e2e8eed_o.jpg',
                       'https://live.staticflickr.com/65535/50064411221_6564587552_o.jpg']

    @pre_operator(name=f"{encoder_name}2", type=encoder_type, addr=encoder_addr, version="0.1", description="")
    @pre_instance(operator_name=f"{encoder_name}2", name=f"{encoder_instance}2")
    @pre_instance(operator_name=f"{encoder_name}2", name=f"{encoder_instance2}2")
    @pre_operator(name=f"{detector_name}2", type=detector_type, addr=detector_addr, version="0.1", description="")
    @pre_instance(operator_name=f"{detector_name}2", name=f"{detector_instance}2")
    @pre_pipeline(name=f"{pipeline_name1}2",
                  encoder={"name": f"{encoder_name}2", "instance": f"{encoder_instance}2"})
    @pre_pipeline(name=f"{pipeline_name2}2",
                  processors=[{"name": f"{detector_name}2", "instance": f"{detector_instance}2"}],
                  encoder={"name": f"{encoder_name}2", "instance": f"{encoder_instance2}2"})
    @pre_application(name=f"{name}",
                     fields={field_name1: {"type": "pipeline", "value": f"{pipeline_name1}2"},
                             field_name2: {"type": "pipeline", "value": f"{pipeline_name2}2"}},
                     s3_buckets=f"s3example{test_ver}")
    @sleep_time(12)  # wait for operator instance initialization
    def test_inner_field_score_api(self, client):
        for image_url in self.test_url:
            data = {
                'fields': {
                    self.field_name2: {
                        'url': image_url
                    }
                }
            }
            rv = client.post(f"/v1/application/{self.name}/upload", json=data)
            assert rv.status_code == 200
        time.sleep(1)  # wait for milvus

        # search in empty milvus collection
        data = {
            'fields': {
                self.field_name1: {
                    'url': self.test_search_url[0],
                    'inner_field_score_mode': "first"
                }
            },
            'topk': 3,
            'nprobe': 10
        }
        rv = client.post(f"/v1/application/{self.name}/search", json=data)
        assert rv.status_code != 200

        # search with nonexist field
        data = {
            'fields': {
                "wrong_field": {
                    'url': self.test_search_url[0],
                    'inner_field_score_mode': "first"
                }
            },
            'topk': 3,
            'nprobe': 10
        }
        rv = client.post(f"/v1/application/{self.name}/search", json=data)
        assert rv.status_code != 200

        # test inner filed score mode search
        for inner_field_score_mode in self.inner_fields:
            data = {
                'fields': {
                    self.field_name2: {
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

        # test score function insufficent topk search
        topk = len(self.test_url) * 10
        for inner_field_score_mode in self.inner_fields:
            data = {
                'fields': {
                    self.field_name2: {
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

        # get and delete all entities
        rv = client.get(f"/v1/application/{self.name}/entity?num=100")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']

    @pre_operator(name=f"{encoder_name}3", type=encoder_type, addr=encoder_addr, version="0.1", description="")
    @pre_instance(operator_name=f"{encoder_name}3", name=f"{encoder_instance}3")
    @pre_instance(operator_name=f"{encoder_name}3", name=f"{encoder_instance2}3")
    @pre_operator(name=f"{detector_name}3", type=detector_type, addr=detector_addr, version="0.1", description="")
    @pre_instance(operator_name=f"{detector_name}3", name=f"{detector_instance}3")
    @pre_pipeline(name=f"{pipeline_name1}3",
                  encoder={"name": f"{encoder_name}3", "instance": f"{encoder_instance}3"})
    @pre_pipeline(name=f"{pipeline_name2}3",
                  processors=[{"name": f"{detector_name}3", "instance": f"{detector_instance}3"}],
                  encoder={"name": f"{encoder_name}3", "instance": f"{encoder_instance2}3"})
    @pre_application(name=f"{name}1",
                     fields={field_name1: {"type": "pipeline", "value": f"{pipeline_name1}3"},
                             field_name2: {"type": "pipeline", "value": f"{pipeline_name2}3"}},
                     s3_buckets=f"s3example{test_ver}")
    @sleep_time(12)  # wait for operator instance initialization
    def test_score_api(self, client):
        for image_url in self.test_url:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': image_url
                    },
                    self.field_name2: {
                        'url': image_url
                    }
                }
            }
            rv = client.post(f"/v1/application/{self.name}1/upload", json=data)
            assert rv.status_code == 200
        time.sleep(1)  # wait for milvus

        # test multi field score function
        topk = len(self.test_url) - 1
        for score_mode in self.score_modes:
            data = {
                'fields': {
                    self.field_name1: {
                        'url': self.test_search_url[0],
                        'inner_field_score_mode': 'first',
                        'weight': 6
                    },
                    self.field_name2: {
                        'url': self.test_search_url[1],
                        'inner_field_score_mode': 'random',
                        'weight': 2
                    },
                    "score_mode": score_mode
                },
                'topk': topk,
                'nprobe': 10
            }
            rv = client.post(f"/v1/application/{self.name}1/search", json=data)
            assert rv.status_code == 200
            json_data = rv.get_json()
            assert len(json_data) == topk

        # get and delete all entities
        rv = client.get(f"/v1/application/{self.name}1/entity?num=100")
        assert rv.status_code == 200
        json_data = rv.get_json()
        for data in json_data:
            reply = client.delete(
                f"/v1/application/{self.name}1/entity/{data['_id']}")
            assert reply.status_code == 200
            json_reply = reply.get_json()
            assert json_reply['_id'] == data['_id']
