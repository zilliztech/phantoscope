import ast


class Mapping:
    def __init__(self, id, app_name, image_url, fields):
        self._id = id
        self._app_name = app_name
        self._image_url = image_url
        self._fields = fields

def new_mapping_ins(id, app_name, image_url, fields):
    if isinstance(fields, str):
        fields = ast.literal_eval(fields)
    return Mapping(id=id, app_name=app_name, image_url=image_url,
                   fields=fields)
