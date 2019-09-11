import json
class JWKSModel:
    use = None
    kid = None
    e = None
    n = None
    x5c = []
    alg = None
    
    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)

        