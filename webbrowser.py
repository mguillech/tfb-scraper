import sys
import logging
import logging.config
from datetime import datetime
from cookiejar import CookieJar
from webpage import WebPage
from webbrowserexception import WebBrowserException
from networkaccessmanager import NetworkAccessManager
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *

class WebBrowser(QObject):    
    def __init__(self):
        logging.debug("-->")
        super(WebBrowser, self).__init__()
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(False)
        self.event_loop = QEventLoop()
        self.cookie_jar = CookieJar()
        self.proxy = QNetworkProxy(QNetworkProxy.HttpProxy, "127.0.1.1", 8888)
        self.network_manager = NetworkAccessManager() 
        self.network_manager.setCookieJar(self.cookie_jar)
        # self.network_manager.setProxy(self.proxy)
        self.web_page = WebPage()        
        self.web_page.setNetworkAccessManager(self.network_manager)
        self.web_view = QWebView()
        self.web_view.setPage(self.web_page)        
        self.web_view.settings().setAttribute(QWebSettings.AutoLoadImages,False)
        self.web_view.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebSettings.JavascriptEnabled, True)
        self.web_view.settings().setAttribute(QWebSettings.XSSAuditingEnabled, False)
        self.web_view.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True) 
        self.connect(self.web_view.page().networkAccessManager(),SIGNAL("finished(QNetworkReply*)"),self.network_reply_finished)
        self.page_loaded_validator = None
        self.page_loaded_handler = None
        self.page_loaded_handler_kwargs = None
        self.timeout_message = None
        self.timer = None
        self.event_loop_exception = None
        logging.debug("<--")
                
    def network_reply_finished(self,reply):
        logging.debug("Reply received for: " + reply.request().url().toString())
        self.network_manager.request_queue[reply.request().url()] = "Completed"
        redirect_url = self.get_redirect_url(reply.attribute(QNetworkRequest.RedirectionTargetAttribute),reply.request().url())
        if redirect_url is not None:
            self.redirect(redirect_url,reply.request())
            
    def redirect(self,url,request):
        frame = self.find_frame_to_redirect(self.web_view.page().mainFrame(),request)
        if frame is not None:
            logging.debug("Redirecting to: " + url.toString())
            frame.load(url)                
    
    def find_frame_to_redirect(self,frame,request):
        if frame.requestedUrl() == request.url():
            return frame
        else:
            children = frame.childFrames()
            for child in children:
                frame_to_redirect = self.find_frame_to_redirect(child,request)
                if frame_to_redirect is not None:
                    return frame_to_redirect
            
    def get_redirect_url(self,possible_redirect_url, orig_requested_url):
        if possible_redirect_url is not None:
            if possible_redirect_url.isRelative():
                if orig_requested_url.isRelative():
                    return None
                possible_redirect_url.setScheme(orig_requested_url.scheme())
                possible_redirect_url.setHost(orig_requested_url.host())
            if orig_requested_url != possible_redirect_url:
                return possible_redirect_url
        
    def get_cookies(self):
        cookies = self.cookie_jar.allCookies()
        raw_cookies = []
        first = True
        for cookie in cookies:
            raw_cookies.append(cookie.toRawForm())
        return raw_cookies
        
    def set_cookies(self,raw_cookies):
        cookies = []
        for raw_cookie in raw_cookies:
            cookie_list = QNetworkCookie.parseCookies(raw_cookie)
            for cookie in cookie_list:
                cookies.append(cookie)
        self.cookie_jar.setAllCookies(cookies)
            
    def cleanup(self):
        logging.debug("-->")
        self.disconnect(self.web_view.page().networkAccessManager(),SIGNAL("finished(QNetworkReply*)"),self.network_reply_finished)        
        self.web_view.setParent(None)
        self.web_page.setParent(None)
        self.network_manager.setParent(None)        
        self.event_loop.setParent(None)
        self.setParent(None)        
        del self.web_view
        del self.web_page
        del self.network_manager
        del self.event_loop
        del self.app
        logging.debug("<--")
