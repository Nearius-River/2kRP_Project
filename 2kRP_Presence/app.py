import logging
import threading
import sys
from PySide6.QtWidgets import QApplication
from interface.qtui import MainWindow
from server.server import create_app
from werkzeug.serving import make_server
from presence.presence import run_presence
from utils.utils import get_translated_string
from app_context import set_main_window

# Configure logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

# Event to signal stopping threads
stop_flag = threading.Event()

class FlaskThread(threading.Thread):
    """Thread to run the Flask server."""
    def __init__(self):
        super().__init__()
        self.server = make_server('0.0.0.0', 7789, create_app())
        self.context = self.server.app.app_context()
        self.context.push()

    def run(self):
        print(get_translated_string('flask_start'))
        self.server.serve_forever()

    def shutdown(self):
        print(get_translated_string('flask_end'))
        self.server.shutdown()

def greet_user():
    print(get_translated_string('greeting'))

if __name__ == '__main__':
    # Initialize the Qt application.
    app = QApplication(sys.argv)
    window = MainWindow()
    set_main_window(window)
    if not window.settings.value('start_minimized', True, type=bool):
        window.show()
        window.activateWindow()
    else:
        window.close()
        
    greet_user()
        
    # Run the Flask app in a separate thread
    flask_thread = FlaskThread()
    flask_thread.start()

    # Run the presence update loop in a separate thread
    presence_thread = threading.Thread(target=run_presence, args=(stop_flag,))
    presence_thread.start()
    
    exit_code = app.exec()

    # Wait for the Qt application to finish
    stop_flag.set()
    flask_thread.shutdown()
    flask_thread.join()
    presence_thread.join()
    
    sys.exit(exit_code)