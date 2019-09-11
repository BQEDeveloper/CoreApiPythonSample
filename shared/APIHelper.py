from models.HttpResponseModel import HttpResponseModel
from models.HttpHeaderModel import HttpHeaderModel
import requests

class APIHelper:
    
    @staticmethod
    def Get(url, httpHeader): 
        try:
            httpResponse = HttpResponseModel()
            headers = {
                'User-Agent' : httpHeader.userAgent,
                'Content-Type' : httpHeader.contentType
            }
            if httpHeader.authorization != None :
                headers.update({'Authorization' : httpHeader.authorization })
            response = requests.get(
                url, headers = headers
            )
            httpResponse.header_code = response.status_code
            httpResponse.body = response.content
            httpResponse.header = response.headers
            httpResponse.response = response
            return httpResponse

        except Exception:
            raise

    @staticmethod
    def Post(url, data, httpHeader): 
        try:
            httpResponse = HttpResponseModel()
            headers = {
                'User-Agent' : httpHeader.userAgent,
                'Content-Type' : httpHeader.contentType
            }
            if httpHeader.authorization != None :
                headers.update({'Authorization' : httpHeader.authorization })
            response = requests.post(
                url, headers = headers, data = data
            )
            httpResponse.header_code = response.status_code
            httpResponse.body = response.content
            httpResponse.header = response.headers
            httpResponse.response = response
            return httpResponse

        except Exception:
            raise
    
    @staticmethod
    def Put(url, data, httpHeader): 
        try:
            httpResponse = HttpResponseModel()
            headers = {
                'User-Agent' : httpHeader.userAgent,
                'Content-Type' : httpHeader.contentType
            }
            if httpHeader.authorization != None :
                headers.update({'Authorization' : httpHeader.authorization })
            response = requests.put(
                url, headers = headers, data = data
            )
            httpResponse.header_code = response.status_code
            httpResponse.body = response.content
            httpResponse.header = response.headers
            httpResponse.response = response
            return httpResponse

        except Exception:
            raise
    
    @staticmethod
    def Delete(url, httpHeader): 
        try:
            httpResponse = HttpResponseModel()
            headers = {
                'User-Agent' : httpHeader.userAgent,
                'Content-Type' : httpHeader.contentType
            }
            if httpHeader.authorization != None :
                headers.update({'Authorization' : httpHeader.authorization })
            response = requests.delete(
                url, headers = headers
            )
            httpResponse.header_code = response.status_code
            httpResponse.body = response.content
            httpResponse.header = response.headers
            httpResponse.response = response
            return httpResponse

        except Exception:
            raise