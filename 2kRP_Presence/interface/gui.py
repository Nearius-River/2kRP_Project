import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import json
import pystray
from PIL import Image

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2kRP")
        self.geometry("400x300")
        self.configure(bg='#d3d3d3')
        
        # Set window icon
        base_path = os.path.dirname(__file__)
        icon_path = os.path.join(base_path, 'madotsuki.ico')
        self.iconbitmap(icon_path)

        # Load preferences from file
        self.preferences = self.load_preferences()

        # Create widgets
        self.create_widgets()

        # Create system tray icon
        image = Image.open(icon_path)
        menu = pystray.Menu(
            pystray.MenuItem('Show', self.show_window),
            pystray.MenuItem('Exit', self.exit_window)
        )
        self.tray_icon = pystray.Icon('2kRP', image, '2kRP', menu)
        self.tray_icon.run_detached()

    def load_preferences(self):
        """Loads preferences from preferences.json or creates a new file with defaults."""
        try:
            with open("preferences.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "real_world_text": "Real World",
                "dream_world_text": "Dream World",
                "location_text": "In: $location",
                "minigame_text": "Playing a minigame",
                "large_image_text": "$playersonline Players Online - $playersonmap on Current Map",
                "small_image_text": "2kRP v1.1"
            }

    def create_widgets(self):
        # Main container
        container = ttk.Notebook(self)
        container.pack(expand=True, fill='both')

        # Start screen
        start_frame = ttk.Frame(container)
        container.add(start_frame, text="Home")
        
        # App name
        app_name_label = ttk.Label(start_frame, text="Yume 2kki Rich Presence (2kRP)", font=("Helvetica", 16))
        app_name_label.pack(pady=10)

        # App version
        version_label = ttk.Label(start_frame, text="Version 1.1", font=("Helvetica", 12))
        version_label.pack(pady=10)

        # Server control
        server_control_frame = ttk.Frame(start_frame)
        server_control_frame.pack(pady=20)

        server_status_label = ttk.Label(server_control_frame, text="Improvements coming to this soon (I swear!)", font=("Helvetica", 12))
        server_status_label.pack(side="left", padx=10)

        # Minimize to tray button
        minimize_button = ttk.Button(server_control_frame, text="Minimize to Tray", command=self.minimize_to_tray)
        minimize_button.pack(side="left", padx=10)

        # Configuration screen
        settings_frame = ttk.Frame(container)
        container.add(settings_frame, text="Configurations")

        # Configuration options
        config_label = ttk.Label(settings_frame, text="Configurations", font=("Helvetica", 16))
        config_label.pack(pady=10)

        # Frame to hold the options
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(pady=10)

        # Create text boxes with labels
        self.entry_widgets = []
        for i, (key, value) in enumerate(self.preferences.items()):
            frame = ttk.Frame(options_frame)
            frame.pack(fill='x')

            label = ttk.Label(frame, text=f"{key}:", font=("Helvetica", 12))
            label.pack(side="left", padx=5)

            entry = ttk.Entry(frame)
            entry.insert(0, value)
            entry.pack(side="left", padx=5, expand=True, fill='x')

            self.entry_widgets.append((label, entry, key))

        # Save button
        save_button = ttk.Button(settings_frame, text="Save", command=self.save_settings)
        save_button.pack(pady=20)

    def toggle_server(self):
        messagebox.showinfo("Server", "Example.")

    def save_settings(self):
        """Validates and saves settings to preferences.json."""
        new_preferences = {}
        for _, entry, key in self.entry_widgets:
            value = entry.get()
            new_preferences[key] = value

        try:
            with open("preferences.json", "w") as f:
                json.dump(new_preferences, f, indent=4)
            messagebox.showinfo("Configurations", "Preferences saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {e}")
    
    def on_tray_icon_clicked(self, icon, item):
        if item.text == 'Show':
            self.show_window()
        elif item.text == 'Exit':
            self.exit_window()

    def minimize_to_tray(self):
        self.withdraw()
        self.tray_icon.visible = True

    def show_window(self):
        self.deiconify()
        self.tray_icon.visible = False

    def exit_window(self):
        self.destroy()
        self.tray_icon.stop()