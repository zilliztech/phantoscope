import time
import pytest
from test_basic import client
from test_basic import local_ip
from utils.require import pre_operator, pre_instance, pre_pipeline, pre_application


class TestScoreFunctionApi:
    """test class for application api"""
    test_ver = 8
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
    test_url = ['https://dss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1906469856,4113625838&fm=26&gp=0.jpg',
                'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592371648552&di=28d2be13f40539aacaa81ab5f43642e6&imgtype=0&src=http%3A%2F%2Fphotocdn.sohu.com%2F20151130%2Fmp45332712_1448864892504_4.jpeg',
                'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1592375248588&di=13521ac5965776e504dde2e242610293&imgtype=0&src=http%3A%2F%2Ft8.baidu.com%2Fit%2Fu%3D2388511970%2C557698405%26fm%3D193',
                'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1668363641,4252982095&fm=26&gp=0.jpg']

    test_search_url = ['https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=3442599741,2386083112&fm=26&gp=0.jpg',
                       'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1389311444,3919902992&fm=26&gp=0.jpg']

    # @pre_operator(name=f"{encoder_name}2", type=encoder_type, addr=encoder_addr, version="0.1", description="")
    # @pre_instance(operator_name=f"{encoder_name}2", name=f"{encoder_instance}2")
    # @pre_instance(operator_name=f"{encoder_name}2", name=f"{encoder_instance2}2")
    # @pre_operator(name=f"{detector_name}2", type=detector_type, addr=detector_addr, version="0.1", description="")
    # @pre_instance(operator_name=f"{detector_name}2", name=f"{detector_instance}2")
    # @pre_pipeline(name=f"{pipeline_name1}2",
    #               encoder={"name": f"{encoder_name}2", "instance": f"{encoder_instance}2"})
    # @pre_pipeline(name=f"{pipeline_name2}2",
    #               processors={"name": f"{detector_name}2", "instance": f"{detector_instance}2"},
    #               encoder={"name": f"{encoder_name}2", "instance": f"{encoder_instance2}2"})
    # @pre_application(name=f"{name}",
    #                  fields={field_name1: {"type": "pipeline", "value": f"{pipeline_name1}2"},
    #                          field_name2: {"type": "pipeline", "value": f"{pipeline_name2}2"}},
    #                  s3_buckets=f"s3example{test_ver}")
    # def test_inner_field_score_api(self, client):
    #     time.sleep(12)  # wait for operator instance initialization  # wait for operator instance initialization
    #     for image_url in self.test_url:
    #         data = {
    #             'fields': {
    #                 self.field_name1: {
    #                     'url': image_url
    #                 }
    #             }
    #         }
    #         rv = client.post(f"/v1/application/{self.name}/upload", json=data)
    #         assert rv.status_code == 200
    #     time.sleep(1)  # wait for milvus
    #     # test inner filed score mode search
    #     for inner_field_score_mode in self.inner_fields:
    #         data = {
    #             'fields': {
    #                 self.field_name1: {
    #                     'url': self.test_search_url[0],
    #                     'inner_field_score_mode': inner_field_score_mode
    #                 }
    #             },
    #             'topk': 3,
    #             'nprobe': 10
    #         }
    #         rv = client.post(f"/v1/application/{self.name}/search", json=data)
    #         assert rv.status_code == 200
    #         json_data = rv.get_json()
    #         assert len(json_data) == 3
    #
    #     # test score function insufficent topk search
    #     topk = len(self.test_url) * 10
    #     for inner_field_score_mode in self.inner_fields:
    #         data = {
    #             'fields': {
    #                 self.field_name1: {
    #                     'url': self.test_search_url[0],
    #                     'inner_field_score_mode': inner_field_score_mode
    #                 }
    #             },
    #             'topk': topk,
    #             'nprobe': 10
    #         }
    #         rv = client.post(f"/v1/application/{self.name}/search", json=data)
    #         assert rv.status_code == 200
    #         json_data = rv.get_json()
    #         assert len(json_data) > 0
    #         assert len(json_data) < topk
    #
    #     # test multi field score function
    #     topk = len(self.test_url) * 10
    #     for inner_field_score_mode in self.inner_fields:
    #         data = {
    #             'fields': {
    #                 self.field_name1: {
    #                     'url': self.test_search_url[0],
    #                     'inner_field_score_mode': inner_field_score_mode,
    #                     'weight': 6
    #                 },
    #                 self.field_name2: {
    #                     'url': self.test_search_url[1],
    #                     'inner_field_score_mode': inner_field_score_mode,
    #                     'weight': 2
    #                 }
    #             },
    #             'topk': topk,
    #             'nprobe': 10
    #         }
    #         pass
    #
    #     # get and delete all entities
    #     rv = client.get(f"/v1/application/{self.name}/entity?num=100")
    #     assert rv.status_code == 200
    #     json_data = rv.get_json()
    #     for data in json_data:
    #         reply = client.delete(
    #             f"/v1/application/{self.name}/entity/{data['_id']}")
    #         assert reply.status_code == 200
    #         json_reply = reply.get_json()
    #         assert json_reply['_id'] == data['_id']

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
    def test_score_api(self, client):
        time.sleep(12)  # wait for operator instance initialization  # wait for operator instance initialization
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
            rv = client.post(f"/v1/application/{self.name}/upload", json=data)
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
            rv = client.post(f"/v1/application/{self.name}/search", json=data)
            assert rv.status_code == 200
            json_data = rv.get_json()
            assert len(json_data) == topk

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
