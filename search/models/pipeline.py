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


# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from service import db
from common.error import Insert2SQLError, QueryFromSQLError, DeleteFromSQLError, UpdateFromSQLError, NotExistError


class Pipeline(db.Model):
    name = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    description = db.Column(db.String(240), unique=False, nullable=True)
    processors = db.Column(db.String(240), unique=False, nullable=False)
    encoder = db.Column(db.String(240), unique=False, nullable=False)
    input = db.Column(db.String(240), unique=False, nullable=True)
    output = db.Column(db.String(240), unique=False, nullable=True)

    def __repr__(self):
        return '<Pipeline %r>' % self.name


def insert_pipeline(p):
    try:
        db.session.add(p)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("insert to sql error", e.orig.args[-1])


def search_pipeline(name=None):
    try:
        if name:
            res = db.session.query(Pipeline).filter(Pipeline.name==name).first()
        else:
            res = db.session.query(Pipeline, Pipeline.name).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def del_pipeline(name):
    try:
        res = db.session.query(Pipeline).filter(Pipeline.name==name).all()
        db.session.query(Pipeline).filter(Pipeline.name==name).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])
