import os
import sys
import logging
from bottle import run
from settings import ROOT_PATH

sys.path.insert(0, ROOT_PATH)
os.chdir(ROOT_PATH)

import dispatcher

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

dispatcher.setup(ROOT_PATH)
run(host='localhost', port=8000, reloader=True)
