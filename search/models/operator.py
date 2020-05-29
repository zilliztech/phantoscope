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


from service import db
from common.error import QueryFromSQLError, Insert2SQLError, DeleteFromSQLError


class Operator(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    backend = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    input = db.Column(db.String(80), nullable=False)
    output = db.Column(db.String(80), nullable=False)
    dimension = db.Column(db.Integer, nullable=False)
    metric_type = db.Column(db.String(120), nullable=False)
    endpoint = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<name %r>' % self.name


def search_operator(name=None):
    try:
        if name:
            res = db.session.query(Operator).filter(Operator.name == name).first()
        else:
            res = db.session.query(Operator, Operator.name).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def insert_operator(operator):
    try:
        db.session.add(operator)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("Insert operator to sql error", e.orig.args[-1])


def del_operator(name):
    try:
        res = db.session.query(Operator).filter(Operator.name == name).first()
        db.session.query(Operator).filter(Operator.name == name).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])
