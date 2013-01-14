import re
import urllib2

from PySide.QtCore import *
from PySide.QtGui import QApplication
import time
import sys

from webbrowser import WebBrowser

def process_iframe_links():
    links.extend([ e.attribute('src') for e in wb.web_view.page().currentFrame().findAllElements('iframe')
                   if 'soundcloud.com' in e.attribute('src').lower() ])
    wb.event_loop.exit()

def get_sc_link():
    anchor = wb.web_view.page().currentFrame().findFirstElement('a.g-sc-logo')
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
                    streams.append(m.group(1))
    wb.event_loop.exit()

def main():
    wb.web_view.load(QUrl('http://topfloorbeats.com/'))
    # wb.web_view.show()
    timer_process_links.start(10000)
    wb.event_loop.exec_()

    for link in links:
        # print '[INFO] Link: %s' % link
        wb.web_view.load(QUrl.fromEncoded(str(link)))
        # wb.web_view.show()
        timer_get_sc_link.start(10000)
        wb.event_loop.exec_()

    wb.app.exit()
    app.exit()

app = QApplication(sys.argv)
wb = WebBrowser()
timer_process_links = QTimer(wb)
timer_process_links.timeout.connect(process_iframe_links)
timer_get_sc_link = QTimer(wb)
timer_get_sc_link.timeout.connect(get_sc_link)

for timer in timer_process_links, timer_get_sc_link:
    timer.setSingleShot(True)

links = []
streams = []

if __name__ == "__main__":
    main()
    print '\n'.join(streams)
