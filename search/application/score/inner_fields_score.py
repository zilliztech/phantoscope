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


import math
from enum import Enum
import random
from itertools import chain


class InnerFieldScoreMode(Enum):
    FIRST = 'first'
    # return result of a random entity
    RANDOM = 'random'
    DISTANCE_FIRST = 'distance_first'
    AVG = 'avg'


def get_unique_list(norm_list):
    return sorted(set(norm_list), key=norm_list.index)


def inner_field_score_helper(inner_field_score_mode):
    def first_function(vids, topk):
        return get_unique_list([x.id for x in vids[0]])

    def random_function(vids, topk):
        tmp_random = random.randint(0, len(vids) - 1)
        return get_unique_list([x.id for x in vids[tmp_random]])

    def distance_first_function(vids, topk):
        res = []
        tmp = list(chain(*vids))
        tmp.sort(key=lambda s: (s.distance))
        for i in tmp:
            tmp_id = i.id
            if tmp_id not in res: res.append(tmp_id)
            if len(res) >= topk: break
        return res

    def avg_select_function(vids, topk):
        res = []
        num_entity = len(vids)
        for i in range(num_entity):
            num = math.ceil(topk / (num_entity - i))
            tmp_idx = 0
            for vid in vids[i]:
                if vid.id in res: continue
                res.append(vid.id)
                tmp_idx += 1
                if tmp_idx >= num: break
        return res

    helper = {InnerFieldScoreMode.FIRST: first_function,
              InnerFieldScoreMode.RANDOM: random_function,
              InnerFieldScoreMode.DISTANCE_FIRST: distance_first_function,
              InnerFieldScoreMode.AVG: avg_select_function}
    return helper.get(inner_field_score_mode)
