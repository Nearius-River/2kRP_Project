import json
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
from utils.utils import validate_url
from utils.constants import get_app_name, get_app_version

# Define default colors and styles
DEFAULT_BG = '#ffcccc'  # Soft pink background
ENTRY_BG = '#ffb8b8'    # Slightly darker pink for entry background
TEXT_COLOR = '#333333'  # Dark text color for contrast
BUTTON_BG = '#ff9999'   # Slightly intense pink for buttons
BUTTON_FG = '#ffffff'   # White text for buttons
TOOLTIP_BG = '#f99292'  # Dark pink for tooltip background

PLACEHOLDER_IMAGE = 'https://i.imgur.com/TN8WK7E.png'

class Application(tk.Tk):
    """Main tkinter interface."""
    def __init__(self, stop_flag):
        super().__init__()

        # Initialize constants and settings
        self.title(get_app_name())
        self.version = get_app_version()
        self.geometry('350x600')
        self.configure(background=TOOLTIP_BG)
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

        # Load preferences
        self.preferences = self.load_preferences()

        # Initialize image options
        self.large_image_option = tk.StringVar(value=self.preferences.get('large_image_option', '1'))
        self.large_custom_image_url = tk.StringVar(value=self.preferences.get('large_custom_image_url', ''))
        self.small_image_option = tk.StringVar(value=self.preferences.get('small_image_option', '2'))
        self.small_custom_image_url = tk.StringVar(value=self.preferences.get('small_custom_image_url', ''))
        
        # Create tab contents
        self.create_home_tab()
        self.create_preferences_tab()

        # Update preferences tab
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
            'details_text': 'Presence Details',
            'state_text': 'Presence State',
            'large_image_text': 'Large Image Text',
            'small_image_text': 'Small Image Text'
        }

        tooltips = {
            'details_text': 'The first message that displays below the presence title (YNOProject Online).',
            'state_text': 'The second message that displays below details.',
            'large_image_text': 'The text that displays when hovering the large image.',
            'small_image_text': 'The text that displays when hovering the small image.'
        }

        # Create entries and labels for settings
        for i, (setting, label_text) in enumerate(settings_labels.items()):
            label = ttk.Label(self.preferences_tab, text=label_text, style='Custom.TLabel')
            label.grid(row=i+1, column=0, padx=10, pady=5)
            self.create_tooltip(label, tooltips[setting])

            entry = tk.Entry(self.preferences_tab, width=30, bg=ENTRY_BG, fg=TEXT_COLOR)
            entry.grid(row=i+1, column=1, padx=10, pady=5)

            self.settings_entries[setting] = entry

        # Create Radioboxes for large image options
        large_image_label = tk.Label(self.preferences_tab, text='Large Image', font=('Helvetica', 12), bg=DEFAULT_BG, fg=TEXT_COLOR)
        large_image_label.grid(row=len(self.settings_entries)+1, column=0, columnspan=2, pady=5)

        large_image_frame = tk.Frame(self.preferences_tab, bg=DEFAULT_BG)
        large_image_frame.grid(row=len(self.settings_entries)+2, column=0, columnspan=2, pady=5)

        tk.Radiobutton(large_image_frame, text='Use current room image', variable=self.large_image_option, value='1', bg=DEFAULT_BG).pack(anchor='w')
        tk.Radiobutton(large_image_frame, text='Use badge image', variable=self.large_image_option, value='2', bg=DEFAULT_BG).pack(anchor='w')
        large_custom_image_rb = tk.Radiobutton(large_image_frame, text='Use custom image', variable=self.large_image_option, value='3', bg=DEFAULT_BG)
        large_custom_image_rb.pack(anchor='w')

        # Add entry for custom large image URL, initially hidden
        self.large_custom_image_entry = tk.Entry(self.preferences_tab, textvariable=self.large_custom_image_url, width=30, bg=ENTRY_BG, fg=TEXT_COLOR)
        if self.large_image_option.get() == '3':
            self.large_custom_image_entry.grid(row=len(self.settings_entries)+3, column=0, columnspan=2, pady=5)
        
        def on_large_image_option_change(*args):
            if self.large_image_option.get() == '3':
                self.large_custom_image_entry.grid(row=len(self.settings_entries)+3, column=0, columnspan=2, pady=5)
            else:
                self.large_custom_image_entry.grid_forget()

        self.large_image_option.trace('w', on_large_image_option_change)

        # Create Radioboxes for small image options
        small_image_label = tk.Label(self.preferences_tab, text='Small Image', font=('Helvetica', 12), bg=DEFAULT_BG, fg=TEXT_COLOR)
        small_image_label.grid(row=len(self.settings_entries)+4, column=0, columnspan=2, pady=5)

        small_image_frame = tk.Frame(self.preferences_tab, bg=DEFAULT_BG)
        small_image_frame.grid(row=len(self.settings_entries)+5, column=0, columnspan=2, pady=5)

        tk.Radiobutton(small_image_frame, text='Use current room image', variable=self.small_image_option, value='1', bg=DEFAULT_BG).pack(anchor='w')
        tk.Radiobutton(small_image_frame, text='Use badge image', variable=self.small_image_option, value='2', bg=DEFAULT_BG).pack(anchor='w')
        small_custom_image_rb = tk.Radiobutton(small_image_frame, text='Use custom image', variable=self.small_image_option, value='3', bg=DEFAULT_BG)
        small_custom_image_rb.pack(anchor='w')

        # Add entry for custom small image URL, initially hidden
        self.small_custom_image_entry = tk.Entry(self.preferences_tab, textvariable=self.small_custom_image_url, width=30, bg=ENTRY_BG, fg=TEXT_COLOR)
        if self.small_image_option.get() == '3':
            self.small_custom_image_entry.grid(row=len(self.settings_entries)+6, column=0, columnspan=2, pady=5)
        
        def on_small_image_option_change(*args):
            if self.small_image_option.get() == '3':
                self.small_custom_image_entry.grid(row=len(self.settings_entries)+6, column=0, columnspan=2, pady=5)
            else:
                self.small_custom_image_entry.grid_forget()

        self.small_image_option.trace('w', on_small_image_option_change)

        # Add save button
        save_button = tk.Button(
            self.preferences_tab,
            text='Save',
            command=self.save_preferences,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            width=20
        )
        save_button.grid(row=len(self.settings_entries)+7, column=0, columnspan=2, pady=10)

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
        self.large_image_option.set(self.preferences.get('large_image_option', '1'))
        self.large_custom_image_url.set(self.preferences.get('large_custom_image_url', ''))
        self.small_image_option.set(self.preferences.get('small_image_option', '2'))
        self.small_custom_image_url.set(self.preferences.get('small_custom_image_url', ''))

    def save_preferences(self):
        """Saves entries from settings tab into the preferences file."""
        for setting, entry in self.settings_entries.items():
            self.preferences[setting] = entry.get()
        self.preferences['large_image_option'] = self.large_image_option.get()
        self.preferences['large_custom_image_url'] = self.large_custom_image_url.get()
        self.preferences['small_image_option'] = self.small_image_option.get()
        self.preferences['small_custom_image_url'] = self.small_custom_image_url.get()
        
        # Validate URLs and set to default if invalid
        if not validate_url(self.preferences['large_custom_image_url']):
            self.preferences['large_custom_image_url'] = PLACEHOLDER_IMAGE
        
        if not validate_url(self.preferences['small_custom_image_url']):
            self.preferences['small_custom_image_url'] = PLACEHOLDER_IMAGE
        
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