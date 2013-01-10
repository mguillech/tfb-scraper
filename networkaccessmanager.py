from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *

class NetworkAccessManager(QNetworkAccessManager):
    def __init__(self):
        self.request_queue = {}
        super(NetworkAccessManager,self).__init__()
        
    def createRequest(self,op,request,outgoingData):
        self.request_queue[request.url()] = "Created" 
        raw_cookie_header = self.cookieJar().getRawCookieHeaderForUrl(request.url())
        request.setRawHeader("Cookie",raw_cookie_header)
        reply = super(NetworkAccessManager,self).createRequest(op,request,outgoingData)
        reply.ignoreSslErrors()
        return reply