_main_window = None

def set_main_window(window):
    """Set the main window for the application context."""
    global _main_window
    _main_window = window
    
def get_main_window():
    """Get the main window for the application context."""
    global _main_window
    if _main_window is None:
        raise ValueError("Main window has not been set.")
    return _main_window