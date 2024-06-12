import json
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
from utils.constants import get_app_name, get_app_version

# Define default colors and styles
DEFAULT_BG = '#ffcccc'  # Soft pink background
ENTRY_BG = '#ffb8b8'    # Slightly darker pink for entry background
TEXT_COLOR = '#333333'  # Dark text color for contrast
BUTTON_BG = '#ff9999'   # Slightly intense pink for buttons
BUTTON_FG = '#ffffff'   # White text for buttons
TOOLTIP_BG = '#f99292'  # Dark pink for tooltip background

class Application(tk.Tk):
    """Main tkinter interface."""
    def __init__(self, stop_flag):
        super().__init__()

        # Initialize constants and settings
        self.title(get_app_name())
        self.version = get_app_version()
        self.geometry('350x350')
        self.stop_flag = stop_flag

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook', background=ENTRY_BG)
        self.style.configure('Custom.TFrame', background=DEFAULT_BG)
        self.style.configure('Custom.TLabel', background=DEFAULT_BG, font=('Helvetica', 10), foreground=TEXT_COLOR)
        self.style.configure('Custom.TButton', background=BUTTON_BG, foreground=BUTTON_FG)

        # Initialize notebook and tabs
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        self.home_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.preferences_tab = ttk.Frame(self.notebook, style='Custom.TFrame')

        self.notebook.add(self.home_tab, text='Home')
        self.notebook.add(self.preferences_tab, text='Preferences')

        # Create tab contents
        self.create_home_tab()
        self.create_preferences_tab()

        # Load and update preferences
        self.preferences = self.load_preferences()
        self.update_preferences_tab()

        # Set window icon
        icon_path = 'images/madotsuki.ico'
        self.iconbitmap(icon_path)

        # Create system tray
        self.tray = pystray.Icon(
            get_app_name(),
            Image.open(icon_path),
            get_app_name(),
            pystray.Menu(pystray.MenuItem('Show', self.restore_window))
        )
        self.tray.run_detached()

        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.terminate)

    def create_home_tab(self):
        title_label = tk.Label(
            self.home_tab,
            text=f'Yume 2kki Rich Presence ({get_app_name()})',
            font=('Helvetica', 16),
            bg=DEFAULT_BG,
            fg=TEXT_COLOR
        )
        title_label.pack(pady=10)

        version_label = tk.Label(
            self.home_tab,
            text=f'App version: {self.version}',
            font=('Helvetica', 10),
            bg=DEFAULT_BG,
            fg=TEXT_COLOR
        )
        version_label.pack(pady=10)

        minimize_button = tk.Button(
            self.home_tab,
            text='Minimize to Tray',
            command=self.minimize_to_tray,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=20
        )
        minimize_button.pack(pady=5)

        stop_button = tk.Button(
            self.home_tab,
            text='Stop',
            command=self.terminate,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=20
        )
        stop_button.pack(pady=5)

    def create_preferences_tab(self):
        title_label = tk.Label(
            self.preferences_tab,
            text='Presence preferences',
            font=('Helvetica', 16),
            bg=DEFAULT_BG,
            fg=TEXT_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Initialize settings entries and labels
        self.settings_entries = {}
        settings_labels = {
            'real_world_text': 'Real World Text',
            'dream_world_text': 'Dream World Text',
            'location_text': 'Location Text',
            'minigame_text': 'Minigame Text',
            'large_image_text': 'Large Image Text',
            'small_image_text': 'Small Image Text'
        }

        tooltips = {
            'real_world_text': 'The message that gets displayed while the player is awake.',
            'dream_world_text': 'The message that will get displayed while the player is dreaming.',
            'location_text': 'Where you currently are in the game. Changes every time you switch to a different room. Displays \"Unknown Location\" if no location is available.',
            'minigame_text': 'The message that gets displayed when you are playing a game in the real world.',
            'large_image_text': 'The text for the large image.',
            'small_image_text': 'The text for the small image.'
        }

        # Create entries and labels for settings
        for i, (setting, label_text) in enumerate(settings_labels.items()):
            label = ttk.Label(self.preferences_tab, text=label_text, style='Custom.TLabel')
            label.grid(row=i+1, column=0, padx=10, pady=5)
            self.create_tooltip(label, tooltips[setting])

            entry = tk.Entry(self.preferences_tab, width=30, bg=ENTRY_BG, fg=TEXT_COLOR)
            entry.grid(row=i+1, column=1, padx=10, pady=5)

            self.settings_entries[setting] = entry

        # Add save button
        save_button = tk.Button(
            self.preferences_tab,
            text='Save',
            command=self.save_preferences,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=20
        )
        save_button.grid(row=len(self.settings_entries)+1, column=0, columnspan=2, pady=10)

    def create_tooltip(self, widget, text):
        """Generates a small tooltip when user hovers the mouse above the label."""
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("300x40")
        tooltip.withdraw()
        label = tk.Label(
            tooltip,
            justify='left',
            wraplength='300',
            text=text,
            width='300',
            height='40',
            background=TOOLTIP_BG,
            fg=TEXT_COLOR,
            relief='solid',
            borderwidth=1,
            font=("Helvetica", 8, "normal")
        )
        label.pack(ipadx=1)

        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def load_preferences(self):
        """Loads preference values from the preferences file."""
        try:
            with open('preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def update_preferences_tab(self):
        """Preloads the entries in settings tab with the preferences value."""
        for setting, entry in self.settings_entries.items():
            entry.delete(0, 'end')
            entry.insert(0, self.preferences.get(setting, ''))

    def save_preferences(self):
        """Saves entries from settings tab into the preferences file."""
        for setting, entry in self.settings_entries.items():
            self.preferences[setting] = entry.get()
        self.save_to_file()

    def save_to_file(self):
        """Saves preferences to 'preferences.json' file."""
        try:
            with open('preferences.json', 'w') as f:
                json.dump(self.preferences, f, indent=4)
            self.show_notification('Preferences have been saved!')
        except Exception as e:
            self.show_notification(f'Could not save preferences: {e}')

    def show_notification(self, message):
        """Displays a non-intrusive notification."""
        notification = tk.Label(
            self,
            text=message,
            font=('Helvetica', 10),
            bg=TOOLTIP_BG,
            fg=TEXT_COLOR
        )
        notification.pack(pady=5)
        self.after(3000, notification.destroy)

    def minimize_to_tray(self):
        """Minimizes the window to the system tray."""
        self.withdraw()
        if not self.tray.visible:
            self.tray.run_detached()

    def restore_window(self):
        """Restores the window from the system tray."""
        self.deiconify()

    def terminate(self):
        """Terminates the application."""
        self.stop_flag.set()
        self.tray.stop()
        self.destroy()

    def start_app(self):
        """Starts the application."""
        self.mainloop()
        self.stop_flag.set()