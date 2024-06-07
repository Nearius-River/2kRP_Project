import json
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pystray
from PIL import Image
from utils.constants import get_app_name, get_app_version

class Application(tk.Tk):
    """Main tkinter interface."""
    def __init__(self, stop_flag):
        super().__init__()
        
        # Constant variables and interface settings
        self.title(get_app_name())
        self.version = get_app_version()
        self.default_bg = '#C2C6D0'
        self.geometry('400x350')
        self.stop_flag = stop_flag
        
        self.notebook = ttk.Notebook(self, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)

        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook', background=self.default_bg)

        # Tab definition
        self.home_tab = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.settings_tab = ttk.Frame(self.notebook, style='Custom.TFrame')

        self.notebook.add(self.home_tab, text='Home')
        self.notebook.add(self.settings_tab, text='Settings')

        self.create_home_tab()
        self.create_settings_tab()

        # Preferences from preferences.json
        self.preferences = self.load_preferences()
        self.update_settings_tab()
        
        # Set window icon
        icon_path = 'images/madotsuki.ico'
        self.iconbitmap(icon_path)
        
        # Create system tray
        menu = pystray.Menu(
            pystray.MenuItem('Show', self.restore_window),
            pystray.MenuItem('Exit', self.terminate)
        )
        image = Image.open(icon_path)
        self.tray = pystray.Icon(get_app_name(), image, get_app_name(), menu)
        self.tray.run_detached()

    def create_home_tab(self):
        title_label = tk.Label(self.home_tab, text=f'Yume 2kki Rich Presence ({get_app_name()})', font=('Arial', 18), bg=self.default_bg)
        title_label.pack(pady=20)

        version_label = tk.Label(self.home_tab, text=f'App version: {self.version}', font=('Arial', 12), bg=self.default_bg)
        version_label.pack(side='bottom', pady=20)

        minimize_button = tk.Button(self.home_tab, text='Minimize to Tray', command=self.minimize_to_tray, bg=self.default_bg, fg='black')
        minimize_button.pack(side='bottom', pady=20)

    def create_settings_tab(self):
        title_label = tk.Label(self.settings_tab, text='Settings', font=('Arial', 18), bg=self.default_bg)
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.settings_entries = {}

        for i, setting in enumerate(['real_world_text', 'dream_world_text', 'location_text', 'minigame_text', 'large_image_text', 'small_image_text']):
            label = tk.Label(self.settings_tab, text=setting, font=('Arial', 12), bg=self.default_bg)
            label.grid(row=i+1, column=0, padx=10, pady=5)

            entry = tk.Entry(self.settings_tab, width=30, bg='#F1E5D1', fg='black')
            entry.grid(row=i+1, column=1, padx=10, pady=5)

            self.settings_entries[setting] = entry

        save_button = tk.Button(self.settings_tab, text='Save', command=self.save_preferences, bg=self.default_bg, fg='black')
        save_button.grid(row=len(self.settings_entries)+1, column=0, columnspan=2, pady=10)

    def load_preferences(self):
        """Loads preference values from the preferences file."""
        try:
            with open('preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def update_settings_tab(self):
        """Preloads the entries in settings tab with the preferences value."""
        for setting, entry in self.settings_entries.items():
            entry.delete(0, 'end')
            entry.insert(0, self.preferences.get(setting, ''))

    def save_preferences(self):
        """Saves entries from settings tab into the preferences file."""
        for setting, entry in self.settings_entries.items():
            self.preferences[setting] = entry.get()
        try:
            with open('preferences.json', 'w') as f:
                json.dump(self.preferences, f, indent=4)
            messagebox.showinfo('Preferences', 'Preferences have been saved!')
        except Exception as e:
            messagebox.showinfo('Error', f'Could not save preferences: {e}')

    def minimize_to_tray(self):
        self.withdraw()

    def restore_window(self):
        self.deiconify()

    def terminate(self):
        """Terminates the tkinter interface and sets stop_flag for other threads to end."""
        self.stop_flag.set()
        self.tray.stop()
        self.destroy()
        
    def start_app(self):
        """Starts the tkinter mainloop() and sets stop_flag upon window closing."""
        self.mainloop()
        self.stop_flag.set()