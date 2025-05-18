import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, 
    QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QComboBox, QSystemTrayIcon,
    QMenu, QMessageBox, QButtonGroup, QRadioButton, QStackedWidget
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QSettings
from qt_material import apply_stylesheet
from utils.utils import validate_url, get_translated_string
from utils.constants import get_app_version
from app_context import set_main_window

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_settings()
        self.init_ui()
        self.init_system_tray()

        # Create tabs
        self.tabs = QTabWidget()
        self.tab_home = QWidget()
        self.tab_presence = QWidget()
        self.tab_settings = QWidget()

        self.tabs.addTab(self.tab_home, get_translated_string("qtui_tab_home"))
        self.tabs.addTab(self.tab_presence, get_translated_string("qtui_tab_presence"))
        self.tabs.addTab(self.tab_settings, get_translated_string("qtui_tab_settings"))

        # Initialize tabs
        self.init_home_tab()
        self.init_presence_tab()
        self.init_settings_tab()

        # Set central widget
        self.setCentralWidget(self.tabs)

    def init_settings(self):
        # Load settings from QSettings
        QSettings.setDefaultFormat(QSettings.IniFormat)
        self.settings = QSettings("2kRP", "2kRP_Presence_Controller")
        
        # Creates default settings if they do not exist
        if not self.settings.contains("start_on_boot"):
            self.settings.setValue("start_on_boot", False)
        if not self.settings.contains("start_minimized"):
            self.settings.setValue("start_minimized", True)
        if not self.settings.contains("theme"):
            self.settings.setValue("theme", "Light")
            
        # Creates presence settings if they do not exist
        if not self.settings.contains("presence"):
            self.settings.setValue("presence", {
                "details": "Playing {gametype}",
                "state": "In: {location}",
                "large_image": "use_current_room",
                "small_image": "use_badge",
                "large_image_text": "{playersonline} players online and {playersonmap} on the current map",
                "small_image_text": "  ",
                "large_image_url": "https://i.imgur.com/TN8WK7E.png",
                "small_image_url": "https://i.imgur.com/TN8WK7E.png",
            })
            
    def init_ui(self):
        self.setWindowTitle("2kRP Presence Controller")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(600, 400)

        file_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(file_path, "icon.png")
        
        self.setWindowIcon(QIcon(icon_path))
        apply_stylesheet(QApplication.instance(), theme="light_pink.xml" if self.settings.value("theme") == "Light" else "dark_pink.xml", invert_secondary=True if self.settings.value("theme") == "Light" else False)

    def init_system_tray(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(file_path, "icon.png")
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        
        tray_menu = QMenu(self)
        show_action = QAction(get_translated_string("qtui_tray_option_show"), self)
        show_action.triggered.connect(self.show_window)
        tray_menu.addAction(show_action)
        
        exit_action = QAction(get_translated_string("qtui_tray_option_exit"), self)
        exit_action.triggered.connect(self.close_app)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
    
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()
    
    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            self.tray_icon.showMessage(
                get_translated_string("qtui_tray_message_title"),
                get_translated_string("qtui_tray_message_text"),
                QSystemTrayIcon.Information,
                2000
            )
            event.ignore()
                
    def show_window(self):
        self.show()
        self.activateWindow()
        
    def close_app(self):
        self.tray_icon.hide()
        self.close()
        QApplication.quit()
    
    def init_home_tab(self):
        layout = QVBoxLayout()
        
        # Labels
        app_title = QLabel("Yume 2kki Rich Presence Controller")
        app_version = QLabel(get_translated_string("qtui_home_app_version") + " " + get_app_version())
        
        app_title.setAlignment(Qt.AlignCenter)
        app_version.setAlignment(Qt.AlignCenter)
        app_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        # Buttons
        minimize_to_tray = QPushButton(get_translated_string("qtui_home_minimize_to_tray"))
        minimize_to_tray.clicked.connect(self.close)
        close_button = QPushButton(get_translated_string("qtui_home_exit"))
        close_button.clicked.connect(self.close_app)
        
        layout.addWidget(app_title)
        layout.addWidget(app_version)
        layout.addWidget(minimize_to_tray)
        layout.addWidget(close_button)
        self.tab_home.setLayout(layout)
        

    def init_presence_tab(self):
        # Define presence tab pages and layouts
        self.page_1 = QWidget()
        self.page_2 = QWidget()
        
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QVBoxLayout()
        
        self.next_page_btn = QPushButton(get_translated_string("qtui_presence_btn_next_page"))
        self.back_page_btn = QPushButton(get_translated_string("qtui_presence_btn_back_page"))
        
        self.page_1.setLayout(self.layout_1)
        self.page_2.setLayout(self.layout_2)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.page_1)
        self.stacked_widget.addWidget(self.page_2)
        
        self.next_page_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.back_page_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.tab_presence.setLayout(main_layout)

        # Presence customization
        self.customization_label = QLabel(get_translated_string("qtui_presence_label_customization"))
        self.customization_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        msgBox = QMessageBox()
        msgBox.setGeometry(100, 100, 600, 300)
        msgBox.setStyleSheet("background-color: #ffcccc;")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(get_translated_string("qtui_presence_msgbox_help_title"))
        msgBox.setText(get_translated_string("qtui_presence_msgbox_help_text"))
        msgBox.setInformativeText(get_translated_string("qtui_presence_msgbox_help_informative_text"))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.button(QMessageBox.Ok).setText(get_translated_string("qtui_presence_msgbox_help_btn"))
        msgBox.button(QMessageBox.Ok).setStyleSheet("background-color: #ff9999;")
        msgBox.button(QMessageBox.Ok).clicked.connect(lambda: msgBox.close())
        
        # Presence fields
        self.details_input = QLineEdit()
        self.details_input.setPlaceholderText(get_translated_string("qtui_presence_placeholder_details"))
        
        self.state_input = QLineEdit()
        self.state_input.setPlaceholderText(get_translated_string("qtui_presence_placeholder_state"))
        
        self.large_image_input = QLineEdit()
        self.large_image_input.setPlaceholderText(get_translated_string("qtui_presence_placeholder_large_image"))
        
        self.small_image_input = QLineEdit()
        self.small_image_input.setPlaceholderText(get_translated_string("qtui_presence_placeholder_small_image"))
        
        # Load existing presence settings
        self.details_input.setText(self.settings.value("presence/details", ""))
        self.state_input.setText(self.settings.value("presence/state", ""))
        self.large_image_input.setText(self.settings.value("presence/large_image_text", ""))
        self.small_image_input.setText(self.settings.value("presence/small_image_text", ""))
        
        # Misc buttons
        self.save_presence_btn = QPushButton(get_translated_string("qtui_presence_btn_save_preferences"))
        self.save_presence_btn.clicked.connect(self.save_presence)
        
        self.help_button = QPushButton(get_translated_string("qtui_presence_btn_help"))
        self.help_button.clicked.connect(msgBox.exec)
        
        # Helper to create radio group for image options
        def create_image_radio_group(prefix):
            radio_group = QButtonGroup(self)
            radio_group.setExclusive(True)

            use_current_room = QRadioButton(get_translated_string("qtui_presence_radio_use_current_room"))
            use_badge = QRadioButton(get_translated_string("qtui_presence_radio_use_badge"))
            use_custom_url = QRadioButton(get_translated_string("qtui_presence_radio_use_custom_url"))

            # Custom URL input
            custom_url_input = QLineEdit()
            custom_url_input.setPlaceholderText(get_translated_string("qtui_presence_placeholder_custom_url"))
            custom_url_input.setEnabled(False)
            use_custom_url.toggled.connect(lambda: custom_url_input.setEnabled(use_custom_url.isChecked()))

            radio_group.addButton(use_current_room)
            radio_group.addButton(use_badge)
            radio_group.addButton(use_custom_url)

            # Set checked state from settings
            value = self.settings.value(f"{prefix}_image")
            if value == "current_room":
                use_current_room.setChecked(True)
            elif value == "badge":
                use_badge.setChecked(True)
            elif value == "custom_url":
                use_custom_url.setChecked(True)
            else:
                use_current_room.setChecked(True)
                
            # Set custom URL from settings
            custom_url = self.settings.value(f"{prefix}_image_url", "https://i.imgur.com/TN8WK7E.png")
            custom_url_input.setText(custom_url)

            return (radio_group, use_current_room, use_badge, use_custom_url, custom_url_input)

        # Large image options
        (self.large_radio_group, self.large_use_current_room, self.large_use_badge,
         self.large_use_custom_url, self.large_use_custom_url_input) = create_image_radio_group("large")

        # Small image options
        (self.small_radio_group, self.small_use_current_room, self.small_use_badge,
         self.small_use_custom_url, self.small_use_custom_url_input) = create_image_radio_group("small")
        
        self.separator_1 = QLabel("")
        self.separator_1.setAlignment(Qt.AlignCenter)
        self.separator_1.setFixedHeight(2)
        self.separator_1.setStyleSheet("background-color: #ffcccc;")
        
        self.separator_2 = QLabel("")
        self.separator_2.setAlignment(Qt.AlignCenter)
        self.separator_2.setFixedHeight(2)
        self.separator_2.setStyleSheet("background-color: #ffcccc;")
        
        self.add_tooltip(self.details_input, get_translated_string("qtui_presence_tooltip_details"))
        self.add_tooltip(self.state_input, get_translated_string("qtui_presence_tooltip_state"))
        self.add_tooltip(self.large_image_input, get_translated_string("qtui_presence_tooltip_large_image"))
        self.add_tooltip(self.small_image_input, get_translated_string("qtui_presence_tooltip_small_image"))

        # Page 1 widgets
        self.layout_1.addWidget(self.customization_label)
        self.layout_1.addWidget(self.details_input)
        self.layout_1.addWidget(self.state_input)
        self.layout_1.addWidget(self.large_image_input)
        self.layout_1.addWidget(self.small_image_input)
        self.layout_1.addWidget(self.save_presence_btn)
        self.layout_1.addWidget(self.help_button)
        self.layout_1.addWidget(self.next_page_btn)
        
        # Page 2 widgets
        self.layout_2.addWidget(QLabel(get_translated_string("qtui_presence_label_large_image_options")))
        self.layout_2.addWidget(self.separator_1)
        self.layout_2.addWidget(self.large_use_current_room)
        self.layout_2.addWidget(self.large_use_badge)
        self.layout_2.addWidget(self.large_use_custom_url)
        self.layout_2.addWidget(self.large_use_custom_url_input)
        self.layout_2.addWidget(QLabel(get_translated_string("qtui_presence_label_small_image_options")))
        self.layout_2.addWidget(self.separator_2)
        self.layout_2.addWidget(self.small_use_current_room)
        self.layout_2.addWidget(self.small_use_badge)
        self.layout_2.addWidget(self.small_use_custom_url)
        self.layout_2.addWidget(self.small_use_custom_url_input)
        self.layout_2.addWidget(self.back_page_btn)
        self.layout_2.addStretch()

    def init_settings_tab(self):
        layout = QVBoxLayout()

        # Settings Widgets
        self.start_on_boot = QCheckBox(get_translated_string("qtui_settings_checkbox_start_on_boot"))
        self.start_minimized = QCheckBox(get_translated_string("qtui_settings_checkbox_start_on_tray"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "Português (BR)"])
        
        # Applies the current settings
        self.start_on_boot.setChecked(self.settings.value("start_on_boot", False, type=bool))
        self.start_minimized.setChecked(self.settings.value("start_minimized", True, type=bool))
        self.theme_combo.setCurrentText(self.settings.value("theme", "Light"))
        
        with open("language.txt", "r", encoding="utf-8") as file:
            language = file.read().strip()
            if language == "en":
                self.language_combo.setCurrentText("English")
            elif language == "pt_br":
                self.language_combo.setCurrentText("Português (BR)")
            else:
                self.language_combo.setCurrentText("English")
        
        # Labels
        self.application_settings_label = QLabel(get_translated_string("qtui_settings_label_application_settings"))
        self.application_settings_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.theme_label = QLabel(get_translated_string("qtui_settings_label_theme"))
        self.theme_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.language_label = QLabel(get_translated_string("qtui_settings_label_language"))
        self.language_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        # Save settings when changed
        self.start_on_boot.stateChanged.connect(lambda: self.settings.setValue("start_on_boot", self.start_on_boot.isChecked()))
        self.start_minimized.stateChanged.connect(lambda: self.settings.setValue("start_minimized", self.start_minimized.isChecked()))
        self.language_combo.currentTextChanged.connect(lambda: self.update_language_code())
        self.theme_combo.currentTextChanged.connect(lambda: self.settings.setValue("theme", self.theme_combo.currentText()))
        self.theme_combo.currentTextChanged.connect(
            lambda: apply_stylesheet(QApplication.instance(), theme="light_pink.xml" if self.theme_combo.currentText() == "Light" else "dark_pink.xml", invert_secondary=True if self.theme_combo.currentText() == "Light" else False)
        )
        
        self.add_tooltip(self.start_on_boot, get_translated_string("qtui_settings_tooltip_start_on_boot"))
        self.add_tooltip(self.start_minimized, get_translated_string("qtui_settings_tooltip_start_on_tray"))
        
        layout.addWidget(self.application_settings_label)
        layout.addWidget(self.start_on_boot)
        layout.addWidget(self.start_minimized)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        layout.addStretch()
        self.tab_settings.setLayout(layout)

    def update_language_code(self):
        """Update the language code based on the selected language."""
        language_code = self.language_combo.currentText()
        if language_code == "English":
            with open("language.txt", "w", encoding="utf-8") as file:
                file.write("en")
        elif language_code == "Português (BR)":
            with open("language.txt", "w", encoding="utf-8") as file:
                file.write("pt_br")
        else:
            with open("language.txt", "w", encoding="utf-8") as file:
                file.write("en")
                
        # Message box to inform the user
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(get_translated_string("qtui_settings_msgbox_language_updated_title"))
        msgBox.setText(get_translated_string("qtui_settings_msgbox_language_updated_text"))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.button(QMessageBox.Ok).clicked.connect(lambda: msgBox.close())
        msgBox.exec()
    
    def save_presence(self):
        self.settings.setValue("presence/details", self.details_input.text())
        self.settings.setValue("presence/state", self.state_input.text())
        self.settings.setValue("presence/large_image_text", self.large_image_input.text())
        self.settings.setValue("presence/small_image_text", self.small_image_input.text())
        
        if not validate_url(self.large_use_custom_url.text()):
            self.large_use_custom_url_input.setText("https://i.imgur.com/TN8WK7E.png")
        
        if not validate_url(self.small_use_custom_url.text()):
            self.small_use_custom_url_input.setText("https://i.imgur.com/TN8WK7E.png")
            
        self.settings.setValue("presence/large_image", "use_current_room" if self.large_use_current_room.isChecked() else "use_badge" if self.large_use_badge.isChecked() else "use_custom_url")
        self.settings.setValue("presence/small_image", "use_current_room" if self.small_use_current_room.isChecked() else "use_badge" if self.small_use_badge.isChecked() else "use_custom_url")
        self.settings.setValue("presence/large_image_url", self.large_use_custom_url_input.text())
        self.settings.setValue("presence/small_image_url", self.small_use_custom_url_input.text())
        self.settings.sync()
        QMessageBox.information(self, get_translated_string("qtui_presence_msgbox_preferences_saved_title"), get_translated_string("qtui_presence_msgbox_preferences_saved_text"), QMessageBox.Ok)
        
        
    def add_tooltip(self, widget, message):
        """Add a tooltip to the widget with a custom message."""
        widget.setToolTip(message)
        widget.setStyleSheet("background-color: #ffcccc;")