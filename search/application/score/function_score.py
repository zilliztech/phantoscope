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


from enum import Enum


# fields
class FunctionScore(Enum):
    WEIGHT = 'weight'


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
            res = min(res, score)
        return res

    def avg_score(scores: list):
        return sum(scores) / len(scores)

    helper = {ScoreMode.SUM: sum_score,
              ScoreMode.MULTIPLE: multiple_score,
              ScoreMode.MAX: max_score,
              ScoreMode.MIN: min_score,
              ScoreMode.AVG: avg_score}
    return helper[score_mode]
