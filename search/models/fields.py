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
from common.error import Insert2SQLError, ExistError, QueryFromSQLError, DeleteFromSQLError


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    app = db.Column(db.String(255), nullable=False)


def insert_fields(fields):
    try:
        exist, name = fields_exist_check(fields)
        if exist:
            raise ExistError(f"field <{name}> had exist", "")
        ids = []
        for field in fields:
            db.session.add(field)
            db.session.flush()
            ids.append(field.id)
        db.session.commit()
        return ids
    except Exception as e:
        if isinstance(e, ExistError):
            raise e
        raise Insert2SQLError("insert fields to sql error", e)


def fields_exist_check(fields):
    if fields:
        app = fields[0].app
    all_name = [x.name for x in db.session.query(Fields).filter(Fields.app == app).all()]
    for field in fields:
        if field.name in all_name:
            return True, field.name
    return False, ""


def search_fields(fields):
    try:
        res = db.session.query(Fields).filter(Fields.id.in_(fields)).all()
        res.sort(key=lambda x: fields.index(x.id))
        return res
    except Exception as e:
        raise QueryFromSQLError("query from sql error", e.orig.args[-1])


def delete_fields(fields):
    try:
        for field in fields:
            db.session.query(Fields).filter(Fields.id == field).delete()
        db.session.commit()
    except Exception as e:
        raise DeleteFromSQLError("delete from sql error", e)
