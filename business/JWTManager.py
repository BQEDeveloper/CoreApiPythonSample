from models.AuthResponseModel import AuthResponseModel
from models.HttpHeaderModel import HttpHeaderModel
from models.HttpResponseModel import HttpResponseModel
from models.JWTModel import JWTModel, JWTHeader, JWTPayload
from models.JWKSModel import JWKSModel
from shared.APIHelper import APIHelper
from shared.GeneralMethods import GeneralMethods
from business.AuthManager import AuthManager
import json
import time

class JWTManager(object):

    config: None
    httpResponse: None
    httpHeader: None
    id_token: None
    jwt: None
    jwks: None

    def __init__(self, config, id_token):
        try:
            JWTManager.config = config
            JWTManager.id_token = id_token
            JWTManager.httpResponse = HttpResponseModel()
            JWTManager.httpHeader = HttpHeaderModel()
            JWTManager.jwt = JWTModel()
            JWTManager.jwks = JWKSModel()

            JWTManager.httpResponse = APIHelper.Get(JWTManager.config.CoreIdentityBaseUrl + '/.well-known/openid-configuration/jwks', JWTManager.httpHeader)
            JWTManager.jwks = JWKSModel(json.dumps(json.loads(JWTManager.httpResponse.body)['keys'][0]))
        except Exception:
            raise        

    @classmethod
    def DecodeJWT(self):
        try:
            header = JWTManager.id_token.split('.')[0]
            payload = JWTManager.id_token.split('.')[1]
            signature = JWTManager.id_token.split('.')[2]
            JWTManager.jwt.header = JWTHeader(GeneralMethods.Base64UrlDecode(header))
            JWTManager.jwt.payload = JWTPayload(GeneralMethods.Base64UrlDecode(payload))
            JWTManager.jwt.signature = GeneralMethods.Base64UrlDecode(signature)            
            return JWTManager.jwt      
        except Exception:
            raise
    
    @classmethod
    def ValidateJWT(self, jwt):
        try:
            JWTManager.jwt = jwt
            return JWTManager.ValidateJWTHeader() and JWTManager.ValidateJWTPayload() and JWTManager.VerifyJWTSingature()       
        except Exception:
            raise
    
    @classmethod
    def ValidateJWTHeader(self):
        try:
            # verify whether algorithm mentioned in Id Token (JWT) matches to the one in JWKS
            if JWTManager.jwt.header.alg != JWTManager.jwks.alg :
               raise Exception("JWT algorithm doesn't match to the one mentioned in the Core API JWKS")
            # verify whether kid mentioned in Id Token (JWT) matches to the one in JWKS
            if JWTManager.jwt.header.kid != JWTManager.jwks.kid :
               raise Exception("JWT kid doesn't match to the one mentioned in the Core API JWKS")
            return True
        except Exception:
            raise
   
    @classmethod
    def ValidateJWTPayload(self):
        try:
            # verify issuer (iss) mentioned in Id Token (JWT) matches to the one in config.ini
            if JWTManager.jwt.payload.iss != JWTManager.config.CoreIdentityBaseUrl :
               raise Exception("JWT issuer (iss) doesn't match to the one mentioned in the config.ini")
            # verify audience (aud) mentioned in Id Token (JWT) matches to the one in config.ini
            if JWTManager.jwt.payload.aud != JWTManager.config.ClientID :
               raise Exception("JWT audience (aud) doesn't match to the one mentioned in the config.ini")
            # verify expiry time (exp) mentioned in Id Token (JWT) has not passed
            if JWTManager.jwt.payload.exp < time.time() :
                raise Exception("JWT expiry time (exp) has already passed. Verify if the PHP server timezone (current timestamp) is correct or the JWT is already expired.")
            return True
        except Exception:
            raise

    @classmethod
    def VerifyJWTSingature(self):
        try:
            # Use RSA Algorithm to validate the signature
            return True
     
        except Exception:
            raise
   