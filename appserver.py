"""
appserver.py
- creates an application instance and runs the dev server
"""

#from near_u.controller import *
from threading import Thread
import time

def pre_start():
    f = open("./near_u/initial", "w")
    f.write("")
    f.close()

if __name__ == '__main__':
    from near_u.application import create_app
    app = create_app()
    pre_start()
    app.run(host='0.0.0.0',ssl_context=('raspberrypi.local.crt', 'raspberrypi.local.key'),use_reloader=False)
