from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *

class CookieJar(QNetworkCookieJar):    
    def setHttpCookiesFromUrl(self,cookieList, url):
        return super(CookieJar,self).setCookiesFromUrl(cookieList,url)
        
    def getRawCookieHeaderForUrl(self,url):
        cookies = super(CookieJar,self).cookiesForUrl(url)
        raw_cookie_header = QByteArray()
        for cookie in cookies:
            raw_cookie_header.append(cookie.name())
            raw_cookie_header.append('=')
            raw_cookie_header.append(cookie.value())
            raw_cookie_header.append(';')
        raw_cookie_header.truncate(raw_cookie_header.length()-1)
        return raw_cookie_header