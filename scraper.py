import re
import urllib2

from PySide.QtCore import *
from PySide.QtGui import QApplication
import time
import sys

from webbrowser import WebBrowser


class TFBScrape(object):
    def __init__(self):
        self.links = []
        self.streams = []
        self.app = QApplication(sys.argv)
        self.wb = WebBrowser()
        self.timer_process_links = QTimer(self.wb)
        self.timer_get_sc_link = QTimer(self.wb)
        self.timer_get_sc_link.timeout.connect(self.get_sc_link)
        self.timer_process_links.timeout.connect(self.process_iframe_links)

        for timer in self.timer_process_links, self.timer_get_sc_link:
            timer.setSingleShot(True)

    def run(self):
        self.wb.web_view.load(QUrl('http://topfloorbeats.com/'))
        # self.wb.web_view.show()
        self.timer_process_links.start(10000)
        self.wb.event_loop.exec_()

        for link in self.links:
            # print '[INFO] Link: %s' % link
            self.wb.web_view.load(QUrl.fromEncoded(str(link)))
            # wb.web_view.show()
            self.timer_get_sc_link.start(10000)
            self.wb.event_loop.exec_()

        self.wb.app.exit()
        self.app.exit()

    def process_iframe_links(self):
        self.links.extend([ e.attribute('src') for e in self.wb.web_view.page().currentFrame().findAllElements('iframe')
                       if 'soundcloud.com' in e.attribute('src').lower() ])
        self.wb.event_loop.exit()

    def get_sc_link(self):
        anchor = self.wb.web_view.page().currentFrame().findFirstElement('a.g-sc-logo')
        if anchor:
            sc_link = anchor.attribute('href')
            if sc_link:
                # print '[INFO] Got SC link: %s' % sc_link
                try:
                    sc_content = urllib2.urlopen(sc_link).read()
                except Exception, e:
                    pass
                    # print "[EXCEPTION] %s" % e.message
                else:
                    m = re.search('streamUrl\":\"(.+?)\",', sc_content)
                    if m:
                        self.streams.append(m.group(1))
        self.wb.event_loop.exit()


if __name__ == "__main__":
    tfb_scraper = TFBScrape()
    tfb_scraper.run()
    print '\n'.join(tfb_scraper.streams)
