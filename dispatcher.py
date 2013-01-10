import os
import logging
import rootcontroller as RootController

from bottle import route, static_file, run, app

# Map request URL's to their handlers
route('/', callback=RootController.get)
route('/get-playlist/', callback=RootController.get_playlist)

# Runs application on local using bottle built-in wsgi
# For local environment only
if __name__ == '__main__':
    static_path = os.path.dirname(os.path.abspath(__file__))
    @route('/img/<filename:path>')
    def send_image(filename):
        return static_file(filename, root=static_path+'/img/')
    @route('/js/<filename:path>')
    def send_js(filename):
        return static_file(filename, root=static_path+'/js/')
    @route('/css/<filename:path>')
    def send_css(filename):
        return static_file(filename, root=static_path+'/css/')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    run(host='localhost', port=8000, reloader=True)
