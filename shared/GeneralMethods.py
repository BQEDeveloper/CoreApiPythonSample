from models.ConfigModel import ConfigModel
from configparser import ConfigParser
import random
import base64

class GeneralMethods:
    
    @staticmethod
    def GetConfig():
        try:
            config = ConfigModel()
            configParser = ConfigParser()

            configParser.read('config.ini')

            config.Secret = configParser['Developer App Config']['Secret']
            config.ClientID = configParser['Developer App Config']['ClientID']
            config.RedirectURI = configParser['Developer App Config']['RedirectURI']

            config.Scopes = configParser['Scopes']['Scopes']

            config.CoreAPIBaseUrl = configParser['urls']['CoreAPIBaseUrl']
            config.CoreIdentityBaseUrl = configParser['urls']['CoreIdentityBaseUrl']

            return config
        except Exception:
            raise

    @staticmethod
    def GenerateRandomString(length = 20):
        try:
            characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+":?><'
            charactersLength = len(characters)
            randomString = ''
            for i in range(0, length):
                randomString += characters[random.randint(0, charactersLength - 1)]          
            return randomString
        except Exception:
            raise
    
    @staticmethod
    def Base64UrlDecode(str):
        try:
            return base64.urlsafe_b64decode(str + '=' * (4 - len(str) % 4))
        except Exception:
            raise