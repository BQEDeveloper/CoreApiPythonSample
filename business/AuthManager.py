from models.AuthResponseModel import AuthResponseModel
from models.HttpHeaderModel import HttpHeaderModel
from models.HttpResponseModel import HttpResponseModel
from shared.APIHelper import APIHelper
from shared.GeneralMethods import GeneralMethods
from flask import session, json
from collections import namedtuple
import urllib
import pickle
import os


class AuthManager(object):

   config: None
   authResponse: None
   httpResponse: None
   httpHeader: None

   def __init__(self):
      try:
         AuthManager.config = GeneralMethods.GetConfig()      
         AuthManager.httpResponse = HttpResponseModel()
         AuthManager.httpHeader = HttpHeaderModel()

         if AuthManager.GetAuthResponse() != None :
            AuthManager.authResponse = AuthManager.GetAuthResponse()
            AuthManager.httpHeader.authorization = 'Bearer ' + AuthManager.authResponse.access_token
      except Exception:
       raise      

   @classmethod
   def ConnectToCore(self):
      try:
            state = GeneralMethods.GenerateRandomString()
            stateObj = { 'state' : state }            
            state = urllib.parse.urlencode(stateObj)            
            session['state'] = state
            return AuthManager.config.CoreIdentityBaseUrl + '/connect/authorize?client_id=' + AuthManager.config.ClientID + '&response_type=code&scope=' + AuthManager.config.Scopes + '&redirect_uri=' + AuthManager.config.RedirectURI + '&' + state
            
      except Exception:
         raise
   
   @classmethod
   def DisconnectFromCore(self):
      try:
         AuthManager.httpHeader.contentType = 'application/x-www-form-urlencoded'
         data = {
            'token': AuthManager.authResponse.access_token,
            'client_id': AuthManager.config.ClientID,
            'client_secret': AuthManager.config.Secret
         }
         AuthManager.httpResponse = APIHelper.Post(AuthManager.config.CoreIdentityBaseUrl + '/connect/revocation', data, AuthManager.httpHeader)
         if AuthManager.httpResponse.header_code == 200 :
            AuthManager.SaveAuthResponse(None)
            return '/'
         else :
            raise Exception(AuthManager.httpResponse.response.content)
         return
      except Exception:
         raise

   @classmethod
   def Authorize(self, code):
      try:
         AuthManager.httpHeader.contentType = 'application/x-www-form-urlencoded'
         data = {
            'code': code,
            'redirect_uri': AuthManager.config.RedirectURI,
            'grant_type': 'authorization_code',
            'client_id': AuthManager.config.ClientID,
            'client_secret': AuthManager.config.Secret
         }
         AuthManager.httpResponse = APIHelper.Post(AuthManager.config.CoreIdentityBaseUrl + '/connect/token', data, AuthManager.httpHeader)
         if AuthManager.httpResponse.header_code == 200 :
            AuthManager.authResponse = AuthResponseModel(AuthManager.httpResponse.body)
         else :
            raise Exception(AuthManager.httpResponse.response.content)
         return AuthManager.authResponse
      except Exception:
         raise

   @classmethod
   def ReAuthorize(self):
      try:
         if AuthManager.GetAuthResponse() != None :
            auth = AuthManager.GetAuthResponse()
            AuthManager.httpHeader.contentType = 'application/x-www-form-urlencoded'
            data = {
               'refresh_token': auth.refresh_token,
               'grant_type': 'refresh_token',
               'client_id': AuthManager.config.ClientID,
               'client_secret': AuthManager.config.Secret
            }
            AuthManager.httpResponse = APIHelper.Post(AuthManager.config.CoreIdentityBaseUrl + '/connect/token', data, AuthManager.httpHeader)
            if AuthManager.httpResponse.header_code == 200 :
               AuthManager.authResponse = AuthResponseModel(AuthManager.httpResponse.body)
               AuthManager.SaveAuthResponse(AuthManager.authResponse)
            else :
               raise Exception(AuthManager.httpResponse.response.content)
            return AuthManager.authResponse         
      except Exception:
         raise

   @classmethod
   def IsValidState(self, state):
      try:
         stateObj = { 'state' : state }
         state = urllib.parse.urlencode(stateObj) 
         return (session['state'] == state)        
      except Exception:
         raise

   @classmethod
   def SaveAuthResponse(self, authResponse):
      try:
         AuthResponseFile = open('AuthResponse.ini', 'wb') 
         if authResponse.endpoint.endswith('/') :
            authResponse.endpoint = authResponse.endpoint.rstrip(authResponse.endpoint[-1])
         pickle.dump(authResponse, AuthResponseFile) 
         AuthResponseFile.close() 
      except Exception:
         raise
   
   @classmethod
   def GetAuthResponse(self):
      try:
         AuthResponseFile = open('AuthResponse.ini', 'rb') 
         if os.path.getsize('AuthResponse.ini') > 0 :
            authResponse = pickle.load(AuthResponseFile)
         else :
            authResponse = None
         AuthResponseFile.close() 
         return authResponse
      except Exception:
         raise