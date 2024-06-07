import logging
import threading
import signal
import sys
from interface.gui import Application
from presence.presence import run_presence
from server.server import create_app
from werkzeug.serving import make_server

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
        self.server.serve_forever()

    def shutdown(self):
        """Shutdown the Flask server."""
        self.server.shutdown()

def signal_handler(sig, frame):
    """Handle SIGINT signal to gracefully shutdown the server and exit."""
    print('Stopping...')
    stop_flag.set()
    flask_thread.shutdown()
    flask_thread.join()
    sys.exit(0)

def greet_user():
    """Print initial user information."""
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

    # Run the presence update loop in a separate thread
    presence_thread = threading.Thread(target=run_presence, args=(stop_flag,))
    presence_thread.start()

    # Create the GUI in a separate thread
    gui_thread = threading.Thread(target=lambda: Application().mainloop())
    gui_thread.start()

    # Wait for the GUI thread to finish
    gui_thread.join()

    # Signal the other threads to stop
    stop_flag.set()

    # Wait for the other threads to finish
    flask_thread.join()
    presence_thread.join()