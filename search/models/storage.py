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


class Storage(db.Model):
    name = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    milvus_addr = db.Column(db.String(120), unique=False, nullable=False)
    milvus_port = db.Column(db.Integer, unique=False, nullable=False)
    milvus_table_name = db.Column(db.String(120), unique=False, nullable=False)
    milvus_dimension = db.Column(db.Integer, unique=False, nullable=False)
    milvus_index_file_size = db.Column(db.Integer, unique=False, nullable=False)
    milvus_metric_type = db.Column(db.String(120), unique=False, nullable=False)
    s3_addr = db.Column(db.String(120), unique=False, nullable=False)
    s3_port = db.Column(db.Integer, unique=False, nullable=False)
    s3_token = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Storage %r>' % self.name
