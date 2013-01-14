import rootcontroller as RootController

from bottle import route, static_file

def setup(root_path):
    # Map request URL's to their handlers
    route('/', callback=RootController.get)
    route('/get-playlist/', callback=RootController.get_playlist)

    @route('/img/<filename:path>')
    def send_image(filename):
        return static_file(filename, root=root_path+'/img/')
    @route('/js/<filename:path>')
    def send_js(filename):
        return static_file(filename, root=root_path+'/js/')
    @route('/css/<filename:path>')
    def send_css(filename):
        return static_file(filename, root=root_path+'/css/')
