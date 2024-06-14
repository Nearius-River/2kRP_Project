import logging
import threading
from interface.gui import Application
from color.colors import print_green
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
        print_green('Flask server established!')
        self.server.serve_forever()

    def shutdown(self):
        """Shutdown the Flask server."""
        print('Flask server has ended.')
        self.server.shutdown()

def greet_user():
    """Print initial user information."""
    print('NOTE: Closing this window will instantly terminate the server connection and undo your current presence on Discord!')
    print('This window will only notify of warnings and errors, if any occurs.')
    print('Have fun travels!')

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