from models.AuthResponseModel import AuthResponseModel
from models.HttpHeaderModel import HttpHeaderModel
from models.HttpResponseModel import HttpResponseModel
from models.UserInfoModel import UserInfoModel
from shared.APIHelper import APIHelper
from shared.GeneralMethods import GeneralMethods
from business.AuthManager import AuthManager
import pickle

class UserInfoManager(object):

    config: None
    authResponse: None
    httpResponse: None
    httpHeader: None
    authManager: None

    def __init__(self):
        try:
            UserInfoManager.config = GeneralMethods.GetConfig()
            UserInfoManager.authResponse = AuthResponseModel()
            UserInfoManager.httpResponse = HttpResponseModel()
            UserInfoManager.httpHeader = HttpHeaderModel()
            UserInfoManager.authManager = AuthManager()

            if AuthManager.GetAuthResponse() != None :
                UserInfoManager.authResponse = AuthManager.GetAuthResponse()
                UserInfoManager.httpHeader.authorization = 'Bearer ' + UserInfoManager.authResponse.access_token
        except Exception:
            raise        

    @classmethod
    def GetUserInfo(self):
        try:
            UserInfoManager.httpResponse = APIHelper.Get(UserInfoManager.config.CoreIdentityBaseUrl + '/connect/userinfo', UserInfoManager.httpHeader)

            if UserInfoManager.httpResponse.header_code == 401 : # UnAuthorised
                UserInfoManager.authResponse = UserInfoManager.authManager.ReAuthorize()
                if UserInfoManager.authResponse != None :
                    UserInfoManager.httpHeader.authorization = "Bearer "+ UserInfoManager.authResponse.access_token
                    return UserInfoManager.GetUserInfo()
            elif UserInfoManager.httpResponse.header_code == 200 : # Success
                userInfo = UserInfoModel(UserInfoManager.httpResponse.body)
                return userInfo  
            else :
                raise Exception(UserInfoManager.httpResponse.response.content)        
        except Exception:
            raise
   