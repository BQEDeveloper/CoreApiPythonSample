from models.AuthResponseModel import AuthResponseModel
from models.HttpHeaderModel import HttpHeaderModel
from models.HttpResponseModel import HttpResponseModel
from models.ActivityModel import ActivityModel
from shared.APIHelper import APIHelper
from shared.GeneralMethods import GeneralMethods
from business.AuthManager import AuthManager
import json
import pickle

class ActivityManager(object):

    config: None
    authResponse: None
    httpResponse: None
    httpHeader: None
    authManager: None

    def __init__(self):
        try:
            ActivityManager.config = GeneralMethods.GetConfig()

            ActivityManager.authResponse = AuthResponseModel()
            ActivityManager.httpResponse = HttpResponseModel()
            ActivityManager.httpHeader = HttpHeaderModel()
            ActivityManager.authManager = AuthManager()

            if AuthManager.GetAuthResponse() != None :
                ActivityManager.authResponse = AuthManager.GetAuthResponse()
                ActivityManager.httpHeader.authorization = 'Bearer ' + ActivityManager.authResponse.access_token
        except Exception:
            raise        

    @classmethod
    def GetList(self):
        try:
            ActivityManager.httpResponse = APIHelper.Get(ActivityManager.config.CoreAPIBaseUrl + '/activity?page=0,100&orderby=name', ActivityManager.httpHeader)

            if ActivityManager.httpResponse.header_code == 401 : # UnAuthorised
                ActivityManager.authResponse = ActivityManager.authManager.ReAuthorize()
                if ActivityManager.authResponse != None :
                    ActivityManager.httpHeader.authorization = "Bearer "+ ActivityManager.authResponse.access_token
                    return ActivityManager.GetList()
            elif ActivityManager.httpResponse.header_code == 200 : # Success
                activityListDict = json.loads(ActivityManager.httpResponse.body)
                activityList = []
                for activityDict in activityListDict: 
                    activity = ActivityModel(json.dumps(activityDict))
                    activityList.append(activity)
                return activityList    
            else :
                raise Exception(ActivityManager.httpResponse.response.content)      
        except Exception:
            raise

    @classmethod
    def Get(self, id):
        try:
            ActivityManager.httpResponse = APIHelper.Get(ActivityManager.config.CoreAPIBaseUrl + '/activity/' + id, ActivityManager.httpHeader)

            if ActivityManager.httpResponse.header_code == 401 : # UnAuthorised
                ActivityManager.authResponse = ActivityManager.authManager.ReAuthorize()
                if ActivityManager.authResponse != None :
                    ActivityManager.httpHeader.authorization = "Bearer "+ ActivityManager.authResponse.access_token
                    return ActivityManager.Get(id)
            elif ActivityManager.httpResponse.header_code == 200 : # Success
                activity = ActivityModel(ActivityManager.httpResponse.body)
                return activity    
            else :
                raise Exception(ActivityManager.httpResponse.response.content)      
        except Exception:
            raise

    @classmethod
    def Create(self, activity):
        try:
            ActivityManager.httpResponse = APIHelper.Post(ActivityManager.config.CoreAPIBaseUrl + '/activity', json.dumps(activity, default = lambda o: o.__dict__), ActivityManager.httpHeader)

            if ActivityManager.httpResponse.header_code == 401 : # UnAuthorised
                ActivityManager.authResponse = ActivityManager.authManager.ReAuthorize()
                if ActivityManager.authResponse != None :
                    ActivityManager.httpHeader.authorization = "Bearer "+ ActivityManager.authResponse.access_token
                    return ActivityManager.Create(activity)
            elif ActivityManager.httpResponse.header_code == 200 or ActivityManager.httpResponse.header_code == 201: # Success or create
                return ActivityManager.httpResponse 
            else :
                raise Exception(ActivityManager.httpResponse.response.content)               
        except Exception:
            raise
   
    @classmethod
    def Update(self, id, activity):
        try:
            ActivityManager.httpResponse = APIHelper.Put(ActivityManager.config.CoreAPIBaseUrl + '/activity/' + id, json.dumps(activity, default = lambda o: o.__dict__), ActivityManager.httpHeader)

            if ActivityManager.httpResponse.header_code == 401 : # UnAuthorised
                ActivityManager.authResponse = ActivityManager.authManager.ReAuthorize()
                if ActivityManager.authResponse != None :
                    ActivityManager.httpHeader.authorization = "Bearer "+ ActivityManager.authResponse.access_token
                    return ActivityManager.Update(id, activity)
            elif ActivityManager.httpResponse.header_code == 200 : # Success
                activity = ActivityModel(ActivityManager.httpResponse.body)
                return activity    
            else :
                raise Exception(ActivityManager.httpResponse.response.content)            
        except Exception:
            raise
    
    @classmethod
    def Delete(self, id):
        try:
            ActivityManager.httpResponse = APIHelper.Delete(ActivityManager.config.CoreAPIBaseUrl + '/activity/' + id, ActivityManager.httpHeader)

            if ActivityManager.httpResponse.header_code == 401 : # UnAuthorised
                ActivityManager.authResponse = ActivityManager.authManager.ReAuthorize()
                if ActivityManager.authResponse != None :
                    ActivityManager.httpHeader.authorization = "Bearer "+ ActivityManager.authResponse.access_token
                    return ActivityManager.Delete(id)
            elif ActivityManager.httpResponse.header_code == 200 or ActivityManager.httpResponse.header_code == 204 : # Success or No-Content
                return ActivityManager.httpResponse 
            else :
                raise Exception(ActivityManager.httpResponse.response.content)         
        except Exception:
            raise