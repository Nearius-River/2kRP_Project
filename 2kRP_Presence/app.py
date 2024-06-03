import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

import threading
import signal
import sys
from presence.presence import run_presence
from server.server import create_app
from werkzeug.serving import make_server

stop_flag = threading.Event()

class FlaskThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 3000, create_app())
        self.context = self.server.app.app_context()
        self.context.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def signal_handler(sig, frame):
    print('Stopping...')
    stop_flag.set()
    flask_thread.shutdown()
    flask_thread.join()
    sys.exit(0)

def greet_user():
    print('NOTE: Closing this window will instantly terminate the server connection and undo your current presence on Discord!')
    print('Press Ctrl+C to close the program at any time (clicking the close button will also do).')
    print('This window will only notify of warnings and errors, if any occurs.')
    print('Have fun travels!')

if __name__ == '__main__':
    greet_user()
    # Set up the signal handler to catch SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Run the Flask app in a separate thread
    flask_thread = FlaskThread()
    flask_thread.start()
    
    # Run the presence update loop in the main thread
    run_presence(stop_flag)