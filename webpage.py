import logging
import logging.config
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *
from PySide.QtNetwork import *

class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, message, lineNumber, sourceID):
       logging.debug('Javascript console message at line number %d\n' % lineNumber)
       logging.debug('%s\n' % message)
       logging.debug('Source ID: %s\n' % sourceID) 
    
    def acceptNavigationRequest(self, frame, request, type):      
        if (request.url().host() == "www.facebook.com"
             or request.url().host() == "connect.facebook.net"
             or request.url().host() == "plusone.google.com"):
            return 0
        logging.debug("Navigating Frame: " + (frame.frameName() if frame is not None else 'Unknown') + " To: " + request.url().toString())
        return 1
        
    def find_first_element(self,selector):
        return self.find_element_in_frame(self.mainFrame(),selector)

    def find_element_in_frame(self,frame,selector):
        element = frame.findFirstElement(selector)
        if element is not None:
            return element
        else:
            children = frame.childFrames()
            for child in children:
                element = self.find_element_in_frame(child,selector)
                if element is not None:
                    return element
                    
    def find_all_elements(self,selector):
        return self.find_elements_in_frame(self.mainFrame(),selector)

    def find_elements_in_frame(self,frame,selector):
        elements = frame.findAllElements(selector)
        if elements is not None:
            if elements.count() > 0:
                return elements
        else:
            children = frame.childFrames()
            for child in children:
                elements = self.find_elements_in_frame(child,selector)
                if elements is not None:
                    if elements.count() > 0:
                        return elements
                        
    def find_frame(self,selector):
        return self._find_frame(self.mainFrame(),selector)
    
    def _find_frame(self,frame,selector):
        element = frame.findFirstElement(selector)
        if element is not None:
            return frame
        else:
            children = frame.childFrames()
            for child in children:
                element = self.find_element_in_frame(child,selector)
                if element is not None:
                    return child