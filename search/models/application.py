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
from common.error import Insert2SQLError, QueryFromSQLError, DeleteFromSQLError, UpdateFromSQLError, NotExistError


class Application(db.Model):
    name = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    fields = db.Column(db.String(255), unique=False, nullable=True)
    s3_buckets = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Application %r>' % self.name


def insert_application(app):
    try:
        db.session.add(app)
        db.session.commit()
    except Exception as e:
        raise Insert2SQLError("insert application to sql error", e.orig.args[-1])


def search_application(name=None):
    try:
        if name:
            res = db.session.query(Application).filter(Application.name == name).first()
        else:
            res = db.session.query(Application, Application.name).all()
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def del_application(name):
    try:
        res = db.session.query(Application).filter(Application.name == name).all()
        db.session.query(Application).filter(Application.name == name).delete()
        db.session.commit()
        return res
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e.orig.args[-1])


def update_application(name, app):
    try:
        old = db.session.query(Application).filter(Application.name == name).first()
        if not old:
            raise NotExistError("update target not exist", "application %s not exist" % name)
        for k, v in app.__dict__.items():
            if v and k != "_sa_instance_state":
                setattr(old, k, v)
        db.session.commit()
        return old
    except Exception as e:
        if isinstance(e, NotExistError):
            raise e
        raise UpdateFromSQLError("update from sql error", e.orig.args[-1])
