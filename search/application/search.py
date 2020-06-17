# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under the License.


import random
import logging
import math
from enum import Enum
from itertools import chain
from application.application import application_detail
from application.mapping import new_mapping_ins
from pipeline.pipeline import pipeline_detail, run_pipeline
from common.error import NoneVectorError
from common.error import RequestError
from common.error import NoneValidFieldError
from common.error import WrongFieldModeError
from common.error import WrongInnerFieldModeError
from storage.storage import MilvusIns
from models.mapping import search_ids_from_mapping

logger = logging.getLogger(__name__)


# fields
class FunctionScore(Enum):
    WEIGHT = 'weight'


class FieldDecayFunction:
    LINEAR = 'linear'


class ScoreMode(Enum):
    FIRST = 'first'
    SUM = 'sum'
    MAX = 'max'
    MIN = 'min'
    MULTIPLE = 'multiple'
    AVG = 'avg'


def score_helper(score_mode: ScoreMode):
    def sum_score(scores: list):
        res = 0
        for score in scores:
            res += score
        return res

    def multiple_score(scores: list):
        res = 1
        for score in scores:
            res *= score
        return res

    def max_score(scores: list):
        res = scores[0]
        for score in scores:
            res = max(res, score)
        return res

    def min_score(scores: list):
        res = scores[0]
        for score in scores:
            res = max(res, score)
        return res

    def avg_score(scores: list):
        return sum(scores) / len(scores)

    helper = {ScoreMode.SUM: sum_score,
              ScoreMode.MULTIPLE: multiple_score,
              ScoreMode.MAX: max_score,
              ScoreMode.MIN: min_score,
              ScoreMode.AVG: avg_score}
    return helper[score_mode]


def decay_helper(decay_function_mode: FieldDecayFunction):
    def linear(number, max, min):
        return list(range(max, min, (max - min) / number))

    helper = {FieldDecayFunction.LINEAR: linear}
    return helper[decay_function_mode]


def get_decay_score(ids, decay_function_mode):
    decay_function = decay_helper(decay_function_mode)
    return decay_function(len(ids), 1, 0.5)


def calc_result_score_list(fields_result, score_config):
    res = {}
    for field, value in fields_result:
        weight = score_config[field]['weight']
        decay_function = score_config[field]['decay_function']
        scores = get_decay_score(value, decay_function)
        for id, score in zip(value, scores):
            res.get(id, []).append(weight * score)
    return res


class InnerFieldScoreMode(Enum):
    FIRST = 'first'
    # return result of a random entity
    RANDOM = 'random'
    DISTANCE_FIRST = 'distance_first'
    AVG = 'avg'


def get_unique_list(norm_list):
    return sorted(set(norm_list), key=norm_list.index)


def get_inner_field_score_result(vids, topk, inner_field_score_mode: InnerFieldScoreMode):
    res = []
    num_entity = len(vids)
    if num_entity == 1:
        return get_unique_list([x.id for x in vids[0]])

    # fix topk number dut to milvus result
    topk = min(topk, len(vids[0]))
    # begin to score
    if inner_field_score_mode == InnerFieldScoreMode.FIRST:
        return get_unique_list([x.id for x in vids[0]])
    if inner_field_score_mode == InnerFieldScoreMode.RANDOM:
        tmp_random = random.randint(0, num_entity - 1)
        return get_unique_list([x.id for x in vids[tmp_random]])
    if inner_field_score_mode == InnerFieldScoreMode.DISTANCE_FIRST:
        tmp = list(chain(*vids))
        tmp.sort(key=lambda s: (s.distance))
        for i in tmp:
            tmp_id = i.id
            if tmp_id not in res: res.append(tmp_id)
            if len(res) >= topk: break
        return res
    if inner_field_score_mode == InnerFieldScoreMode.AVG:
        for i in range(num_entity):
            num = math.ceil(topk / (num_entity - i))
            tmp_idx = 0
            for vid in vids[i]:
                if vid.id in res: continue
                res.append(vid.id)
                tmp_idx += 1
                if tmp_idx >= num: break
        return res
    raise WrongInnerFieldModeError("Unsupported inner field mode", Exception())


def get_score_result(fields_result, topk, score_config, score_mode: str):
    try:
        score_mode = ScoreMode(score_mode)
    except Exception as e:
        raise WrongFieldModeError("Unsupported function score mode", e)

    if len(fields_result) == 1:
        return list(fields_result.values())[0]
    if score_mode == ScoreMode.FIRST:
        return list(fields_result.values())[0]

    uncombined_scores = calc_result_score_list(fields_result, score_config)
    score_combine_function = score_helper(score_mode)
    res = []
    for id, score_list in uncombined_scores.items():
        final_score = score_combine_function(score_list)
        res.append((id, final_score))
        res.sort(key=lambda x: x[1])
    result_ids = [i[0] for i in res]
    return result_ids[:topk]


def search_and_score(milvus_collection_name, vectors, topk, nprobe, inner_score_mode: str):
    '''
    search vectors from milvus and score by inner field score mode
    :param milvus_collection_name: collection name will be search
    :param vectors: vectors which will be searched in milvus
    :param topk: milvus topk number
    :param nprobe: milvus nprobe number
    :param inner_score_mode:
    :return: image id of entity
    '''
    result_dbs = []
    MAX_TOPK = 2048
    magic_number = 60
    increase_rate = 0.1
    query_topk = topk + magic_number
    end_flag = False
    try:
        inner_score_mode = InnerFieldScoreMode(inner_score_mode)
    except Exception as e:
        raise WrongInnerFieldModeError("Unsupported inner field mode", e)
    while (len(result_dbs) < topk) and (not end_flag):
        # check query topk max value
        query_topk = min(query_topk, MAX_TOPK)
        vids = MilvusIns.search_vectors(milvus_collection_name, vectors, topk=query_topk, nprobe=nprobe)
        # filter -1 and if exist -1 or len(vids) < topk
        if (-1 in vids.id_array[0]) or len(vids[0]) < query_topk:
            end_flag = True
        # inner field score function here
        res_vids = get_inner_field_score_result(vids, query_topk, inner_score_mode)

        if len(res_vids) < topk:
            if query_topk < MAX_TOPK:
                # calc a new query_topk and needn't to query from mysql
                query_topk += math.ceil(query_topk * increase_rate)
                increase_rate *= 2
                if not end_flag:
                    continue
            end_flag = True

        result_dbs = search_ids_from_mapping(res_vids)
        # calc a new query_topk if len(result_dbs) < topk
        query_topk += math.ceil(query_topk * increase_rate)

    return result_dbs[:topk]


def search(name, fields={}, topk=10, nprobe=16):
    fields_res = {}
    score_config = {}
    try:
        app = application_detail(name)
        accept_fields = [x for x, y in app.fields.items() if y.get('type') != "object"]
        pipeline_fields = {x: y['pipeline'] for x, y in app.fields.items() if y.get('type') == "object"}

        # check input field is valid
        for k, _ in fields.items():
            if k not in accept_fields and k not in pipeline_fields:
                raise RequestError(f"fields {k} not in application", "")
        valid_field_flag = False
        for n, p in pipeline_fields.items():
            pipe = pipeline_detail(p)

            value = fields.get(n)
            if not value:
                continue

            valid_field_flag = True
            file_data = value.get('data')
            url = value.get('url')
            inner_score_mode = value.get('inner_field_score_mode', 'distance_first')
            score_config[n]['wight'] = value.get('weight', 1)
            score_config[n]['decay_function'] = value.get('decay_function', 'linear')
            if not file_data and not url:
                raise RequestError("can't find data or url from request", "")
            vectors = run_pipeline(pipe, data=file_data, url=url)
            if not vectors:
                raise NoneVectorError("can't encode data by encoder, check input or encoder", "")

            milvus_collection_name = f"{pipe.name}_{pipe.encoder}"
            dbs = search_and_score(milvus_collection_name, vectors, topk, nprobe, inner_score_mode)
            tmp_res = []
            for db in dbs:
                m = new_mapping_ins(id=db.id, app_name=db.app_name,
                                    image_url=db.image_url, fields=db.fields)
                tmp_res.append(m)
            fields_res[n] = tmp_res
        if not valid_field_flag:
            raise NoneValidFieldError("There is none valid field in search request boby", Exception())
        score_mode = fields.get('score_mode', 'first')
        res = get_score_result(fields_res, topk, score_config, score_mode)
        return res
    except Exception as e:
        logger.error("Unexpected error happen when search, %s",
                     str(e), exc_info=True)
        raise e
