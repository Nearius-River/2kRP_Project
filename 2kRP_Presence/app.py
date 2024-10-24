import logging
import threading
from interface.gui import Application
from color.colors import print_green
from presence.presence import run_presence
from server.server import create_app
from werkzeug.serving import make_server
from utils.utils import get_translated_string

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
        """Run the Flask server."""
        print_green(get_translated_string('flask_server_start'))
        self.server.serve_forever()

    def shutdown(self):
        """Shutdown the Flask server."""
        print(get_translated_string('flask_server_end'))
        self.server.shutdown()

def greet_user():
    """Print initial user information."""
    print(get_translated_string('greeting'))

if __name__ == '__main__':
    greet_user()

    # Run the Flask app in a separate thread
    flask_thread = FlaskThread()
    flask_thread.start()

    # Run the presence update loop in a separate thread
    presence_thread = threading.Thread(target=run_presence, args=(stop_flag,))
    presence_thread.start()

    # Create the GUI in a separate thread
    gui_thread = threading.Thread(target=lambda: Application(stop_flag).start_app())
    gui_thread.start()
    
    # Wait for the GUI thread to finish
    gui_thread.join()

    # Wait for all other threads to finish
    flask_thread.shutdown()
    flask_thread.join()
    presence_thread.join()