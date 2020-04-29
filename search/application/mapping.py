import ast


class Mapping:
    def __init__(self, id, app_name, image_url, fields, target_fields):
        self._id = id
        self._app_name = app_name
        self._image_url = image_url
        self._fields = fields
        self._target_fields = target_fields

def new_mapping_ins(id, app_name, image_url, fields, target_fields):
    if isinstance(fields, str):
        fields = ast.literal_eval(fields)
    if isinstance(target_fields, str):
        target_fields = ast.literal_eval(target_fields)
    return Mapping(id=id, app_name=app_name, image_url=image_url,
                   fields=fields, target_fields=target_fields)
