import json
class ActivityModel:
    id = None
    code = None
    description = None
    billable = None
    costRate = None
    billRate = None
    
    def __init__(self, jsonData = '{}') :
        self.__dict__ = json.loads(jsonData)