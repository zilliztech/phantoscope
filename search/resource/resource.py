import uuid
import datetime
import json

class Metadata:
    def __init__(self, id, create_time, resource_type, state):
        self.id = id
        self.create_time = create_time
        self.resource_type = resource_type
        self.state = state

class Resource:
    def _metadata(self, id=None, create_time=None, resource_type=None, state=None):
        if not id:
            id = str(uuid.uuid4())
        if not create_time:
            create_time = str(datetime.datetime.now())
        if not resource_type:
            resource_type = self.__class__.__name__
        if not state:
            state = "created"
        return Metadata(id, create_time, resource_type, state)

    def to_dict(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

def new_resource(id, create_time, resource_type, state):
    return Resource(id, create_time, resource_type, state)
