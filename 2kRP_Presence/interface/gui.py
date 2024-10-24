import json
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
from utils.utils import validate_url, get_translated_string, get_settings
from utils.constants import get_app_name, get_app_version

# Define default colors and styles
DEFAULT_BG = '#ffcccc'
ENTRY_BG = '#ffb8b8'
TEXT_COLOR = '#333333'
BUTTON_BG = '#ff9999'
BUTTON_FG = '#000000'
TOOLTIP_BG = '#f99292'

PLACEHOLDER_IMAGE = 'https://i.imgur.com/TN8WK7E.png'

class Application(tk.Tk):
    """Main tkinter interface."""
    def __init__(self, stop_flag):
        super().__init__()
        self.init_ui()
        self.stop_flag = stop_flag

        # Load preferences
        self.presence_preferences = self.load_presence_preferences()
        self.language = tk.StringVar(value=get_settings().get('language'))

        # Initialize image options
        self.large_image_option = tk.StringVar(value=self.presence_preferences.get('large_image_option', '1'))
        self.large_custom_image_url = tk.StringVar(value=self.presence_preferences.get('large_custom_image_url', ''))
        self.small_image_option = tk.StringVar(value=self.presence_preferences.get('small_image_option', '2'))
        self.small_custom_image_url = tk.StringVar(value=self.presence_preferences.get('small_custom_image_url', ''))

        # Create tab contents
        self.create_home_tab()
        self.create_presence_tab()
        self.create_settings_tab()

        # Update preferences tab
        self.update_presence_tab()

        # Set window icon
        self.set_window_icon('images/madotsuki.ico')

        # Create system tray
        self.create_system_tray('images/madotsuki.ico')

        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.terminate)

    def init_ui(self):
        self.title(get_app_name())
        self.version = get_app_version()
        self.geometry('350x600')
        self.maxsize(350, 600)
        self.minsize(350, 600)
        self.configure(background=TOOLTIP_BG)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook', background=ENTRY_BG)
        self.style.configure('Custom.TFrame', background=DEFAULT_BG)
        self.style.configure('Custom.TLabel', background=DEFAULT_BG, font=('Helvetica', 10), foreground=TEXT_COLOR)
        self.style.configure('Custom.TButton', background=BUTTON_BG, foreground=BUTTON_FG)
        self.style.configure('Custom.TMenu', background=DEFAULT_BG, foreground=TEXT_COLOR)

        # Initialize notebook and tabs
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        self.home_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.presence_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.settings_tab = ttk.Frame(self.notebook, style='Custom.TFrame')

        self.notebook.add(self.home_tab, text=get_translated_string('tkui_tab_home'))
        self.notebook.add(self.presence_tab, text=get_translated_string('tkui_tab_presence'))
        self.notebook.add(self.settings_tab, text=get_translated_string('tkui_tab_settings'))

    def set_window_icon(self, icon_path):
        self.iconbitmap(icon_path)

    def create_system_tray(self, icon_path):
        self.tray = pystray.Icon(
            get_app_name(),
            Image.open(icon_path),
            get_app_name(),
            pystray.Menu(pystray.MenuItem(get_translated_string('tkui_tray_option_show'), self.restore_window))
        )
        self.tray.run_detached()

    def create_home_tab(self):
        self.create_label(self.home_tab, f'Yume 2kki Rich Presence ({get_app_name()})', 16, 10, row=0, column=0)
        self.create_label(self.home_tab, get_translated_string('tkui_home_app_version') + " " + str(self.version), 10, 10, row=1, column=0)
        self.create_button(self.home_tab, get_translated_string('tkui_home_minimize_to_tray'), self.minimize_to_tray, 30, 10, row=2, column=0)
        self.create_button(self.home_tab, get_translated_string('tkui_home_stop'), self.terminate, 30, 10, row=3, column=0)

    def create_presence_tab(self):
        self.create_label(self.presence_tab, get_translated_string('tkui_presence_title'), 16, 10, row=0, column=0, columnspan=2)

        settings_labels = {
            'details_text': get_translated_string('tkui_presence_label_details'),
            'state_text': get_translated_string('tkui_presence_label_state'),
            'large_image_text': get_translated_string('tkui_presence_label_large_image'),
            'small_image_text': get_translated_string('tkui_presence_label_small_image')
        }

        tooltips = {
            'details_text': get_translated_string('tkui_presence_details_tooltip'),
            'state_text': get_translated_string('tkui_presence_state_tooltip'),
            'large_image_text': get_translated_string('tkui_presence_large_image_tooltip'),
            'small_image_text': get_translated_string('tkui_presence_small_image_tooltip')
        }

        self.settings_entries = {}
        for i, (setting, label_text) in enumerate(settings_labels.items()):
            self.create_label(self.presence_tab, label_text, 10, 5, row=i+1, column=0)
            entry = self.create_entry(self.presence_tab, 30, row=i+1, column=1)
            self.create_tooltip(entry, tooltips[setting])
            self.settings_entries[setting] = entry

        self.create_image_option(self.presence_tab, get_translated_string('tkui_presence_image_option_large'), self.large_image_option, self.large_custom_image_url, len(settings_labels)+1)
        self.create_image_option(self.presence_tab, get_translated_string('tkui_presence_image_option_small'), self.small_image_option, self.small_custom_image_url, len(settings_labels)+4)

        self.create_button(self.presence_tab, get_translated_string('tkui_presence_save'), self.save_preferences, 20, 10, row=len(settings_labels)+7, column=0, columnspan=2)

    def create_settings_tab(self):
        self.create_label(self.settings_tab, get_translated_string('tkui_settings_title'), 16, 10, row=0, column=0, columnspan=2)
        
        languages = {"en": "English", "pt_br": "Português"}
        
        self.create_label(self.settings_tab, get_translated_string('tkui_settings_select_language'), 12, 10, row=1, column=0)
        self.create_menu(self.settings_tab, self.language, languages, 10, row=1, column=1)
        self.language.trace_add('write', self.save_settings)
    
    def create_label(self, parent, text, font_size, pady, **grid_opts):
        label = tk.Label(parent, text=text, font=('Helvetica', font_size), bg=DEFAULT_BG, fg=TEXT_COLOR)
        label.grid(pady=pady, **grid_opts)
        return label

    def create_entry(self, parent, width, **grid_opts):
        entry = tk.Entry(parent, width=width, bg=ENTRY_BG, fg=TEXT_COLOR)
        entry.grid(padx=10, pady=5, **grid_opts)
        return entry

    def create_button(self, parent, text, command, width, pady, **grid_opts):
        button = tk.Button(parent, text=text, command=command, bg=BUTTON_BG, fg=BUTTON_FG, width=width)
        button.grid(pady=pady, **grid_opts)
        return button
    
    def create_menu(self, parent, variable, values, pady, **grid_opts):
        menu = tk.OptionMenu(parent, variable, *values)
        menu.configure(bg=ENTRY_BG, fg=TEXT_COLOR, font=("Arial", 12), activebackground=TOOLTIP_BG, activeforeground=BUTTON_FG)
        menu.grid(pady=pady, **grid_opts)
        return menu

    def create_image_option(self, parent, label_text, image_option_var, custom_image_url_var, start_row):
        self.create_label(parent, label_text, 12, 5, row=start_row, column=0, columnspan=2)
        frame = tk.Frame(parent, bg=DEFAULT_BG)
        frame.grid(row=start_row+1, column=0, columnspan=2, pady=5)

        tk.Radiobutton(frame, text=get_translated_string('tkui_presence_radio_option_current_room'), variable=image_option_var, value='current_room', bg=DEFAULT_BG).pack(anchor='w')
        tk.Radiobutton(frame, text=get_translated_string('tkui_presence_radio_option_badge'), variable=image_option_var, value='badge', bg=DEFAULT_BG).pack(anchor='w')
        custom_image_rb = tk.Radiobutton(frame, text=get_translated_string('tkui_presence_radio_option_custom'), variable=image_option_var, value='custom', bg=DEFAULT_BG)
        custom_image_rb.pack(anchor='w')

        custom_image_entry = tk.Entry(parent, textvariable=custom_image_url_var, width=30, bg=ENTRY_BG, fg=TEXT_COLOR)
        if image_option_var.get() == 'custom':
            custom_image_entry.grid(row=start_row+2, column=0, columnspan=2, pady=5)
        
        def on_image_option_change(*args):
            if image_option_var.get() == 'custom':
                custom_image_entry.grid(row=start_row+2, column=0, columnspan=2, pady=5)
            else:
                custom_image_entry.grid_forget()

        image_option_var.trace('w', on_image_option_change)

    def create_tooltip(self, widget, text):
        """Generates a small tooltip when user hovers the mouse above the determined widget."""
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

    def load_presence_preferences(self):
        """Loads presence preference values from the presence file."""
        try:
            with open('presence.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def update_presence_tab(self):
        """Preloads the entries in settings tab with the presence preferences value."""
        for setting, entry in self.settings_entries.items():
            entry.delete(0, 'end')
            entry.insert(0, self.presence_preferences.get(setting, ''))
        self.large_image_option.set(self.presence_preferences.get('large_image_option', '1'))
        self.large_custom_image_url.set(self.presence_preferences.get('large_custom_image_url', ''))
        self.small_image_option.set(self.presence_preferences.get('small_image_option', '2'))
        self.small_custom_image_url.set(self.presence_preferences.get('small_custom_image_url', ''))

    def save_preferences(self):
        """Saves entries from settings tab into the presence preferences file."""
        for setting, entry in self.settings_entries.items():
            self.presence_preferences[setting] = entry.get()
        self.presence_preferences['large_image_option'] = self.large_image_option.get()
        self.presence_preferences['large_custom_image_url'] = self.large_custom_image_url.get()
        self.presence_preferences['small_image_option'] = self.small_image_option.get()
        self.presence_preferences['small_custom_image_url'] = self.small_custom_image_url.get()
        
        # Validate URLs and set to default if invalid
        if not validate_url(self.presence_preferences['large_custom_image_url']):
            self.presence_preferences['large_custom_image_url'] = PLACEHOLDER_IMAGE
        
        if not validate_url(self.presence_preferences['small_custom_image_url']):
            self.presence_preferences['small_custom_image_url'] = PLACEHOLDER_IMAGE
        
        self.save_preferences_to_file()

    def save_preferences_to_file(self):
        """Saves presence preferences to 'presence.json' file."""
        try:
            with open('presence.json', 'w') as f:
                json.dump(self.presence_preferences, f, indent=4)
            self.show_notification(get_translated_string('tkui_notif_preferences_saved'))
        except Exception as e:
            self.show_notification(get_translated_string('tkui_notif_preferences_saved_exception'))
            print(e)
    
    def save_settings(self, *args):
        settings = {"language": self.language.get()}
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=4)
        self.show_notification(get_translated_string('tkui_notif_settings_saved'))

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