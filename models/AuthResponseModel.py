import json
class AuthResponseModel:
    id_token = None
    access_token = None
    expires_in = None
    token_type = None
    refresh_token = None

    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)