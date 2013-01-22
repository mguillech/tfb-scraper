from bottle import request, response, template, static_file, HTTPResponse
import json
import datetime
import os
from settings import ROOT_PATH
from scraper import TFBScrape
from utils import custom_static_file

def get():
    return template('homepage')
    
def get_notfound():
    return template('404')

def get_playlist():
    tfb_scraper = TFBScrape()
    tfb_scraper.run()
    if tfb_scraper.streams:
        filename = datetime.datetime.now().strftime('playlist-%Y%m%d.m3u')
        path = os.path.join('/tmp', filename)
        with open(path, 'w') as fd:
            fd.write('\n'.join(tfb_scraper.streams))
        return custom_static_file(filename, root='/tmp', download=filename,
            custom_headers={'Set-Cookie': 'fileDownload=true; path=/'})
    response.body = 'No streams found.'
    return response