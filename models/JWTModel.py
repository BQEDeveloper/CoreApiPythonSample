import json

class JWTModel:
    header = None
    payload = None
    signature = None

    def __init__(self):
      self.header = JWTHeader()      
      self.payload = JWTPayload()


class JWTHeader:
    alg = None
    kid = None
    typ = None
    x5t = None

    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)
    

class JWTPayload:
    nbf = None
    exp = None
    iss = None
    aud = None
    iat = None
    at_hash = None
    sid = None
    sub = None
    auth_time = None
    idp = None
    amr = []

    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)
    