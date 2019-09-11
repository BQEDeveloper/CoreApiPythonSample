import json
class UserInfoModel:
    sub = None
    email = None
    givenName = None
    name = None
    family_name = None
    phone_number = None
    locale = None
    country = None
    company = None

    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)