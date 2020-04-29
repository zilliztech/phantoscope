from settings.settings_api import settings
#from resource.images_api import images
from application.application_api import application
#from search.search_api import search
#from storage.storage_api import storage
from pipeline.pipeline_api import pipeline
from operators.operators_api import operator
from service import app

app.register_blueprint(settings, url_prefix='/v1/settings')
#app.register_blueprint(images, url_prefix='/v1/images')
#app.register_blueprint(search, url_prefix='/v1/search')
#app.register_blueprint(storage, url_prefix='/v1/storage')
app.register_blueprint(pipeline, url_prefix='/v1/pipeline')
app.register_blueprint(operator, url_prefix='/v1/operator')
app.register_blueprint(application, url_prefix='/v1/application')
