class HttpHeaderModel:
    authorization = None
    contentType = None
    userAgent = None

    def __init__(self):
      self.userAgent = "Mozilla/5.0"      
      self.contentType = "application/json; charset=UTF-8"