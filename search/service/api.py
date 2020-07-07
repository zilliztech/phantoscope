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


from settings.settings_api import settings
from application.application_api import application
from pipeline.pipeline_api import pipeline
from operators.operators_api import operator
from service import app

app.register_blueprint(settings, url_prefix='/v1/settings')
app.register_blueprint(pipeline, url_prefix='/v1/pipeline')
app.register_blueprint(operator, url_prefix='/v1/operator')
app.register_blueprint(application, url_prefix='/v1/application')
