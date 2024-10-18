# 2kRP Project

https://ynoproject.net

This project aims to integrate Discord Rich Presence with YNO games for the navigator, while (hopefully) being lightweight, easy to use and to customize.

It utilizes a browser extension to act as a "linker", whose primary function is to send site data (such as location, player count, current game, etc) to the running Python application on the user's system through a localhost connection.

Most of the data the extension gathers is captured from HTML elements of the site itself.

<div align="center">
    <img src="https://github.com/Nearius-River/2kRP_Project/assets/49107257/d3bdd888-5fb3-43d9-9bba-56c5f0c266f7" alt="Example of how the presence looks.">
</div>

## Project Structure

- `2kRP_Extension/`: Contains the browser extension files.
- `2kRP_Presence/`: Contains the rich presence application. Also handles the local server communication with the extension.

## Installation

### Pre-requisites

- **Python 3.8+** with pip available
- **Chrome/Edge browser** (the extension should work fine on these; not tested on Firefox or other browsers)
- **Discord desktop app** installed and running (for updating the rich presence)

### Instructions (for the Python application)

1. Download and run the `install_script.py` to automatically download and set up all necessary files. This script is available from the project releases.

2. Navigate to the `2kRP_Presence` directory and run the application:

    ```sh
    python app.py
    ```

    Alternatively, you can double-click on "app.py" to open it.

### Instructions (for the browser extension)

1. Open your Chrome or Edge browser:

    - **For Chrome**: Click the three dots menu > Extensions > Manage Extensions > Load unpacked, then select the `2kRP_Extension` folder inside `2kRP_Project-master`.
    
    - **For Edge**: Click the extensions button > Manage Extensions > Load unpacked, then select the `2kRP_Extension` folder inside `2kRP_Project-master`.

## Usage

### Starting the Server

1. **Open `app.py`**:
    - Run `app.py` and keep it open. Closing it will terminate the server connection.
    - If "Connection established!" appears in the terminal, you're connected.

2. **Play a Game**:
    - Visit the YNO site and pick any Yume game.
    - Bam! Your presence will be updated as long as the app is running. Truly magical.

### Switching Application Language

Currently, the application is fully compatible with English and Portuguese (Brazilian). You can change your preferred language through the menu in the settings tab.

### Customizing Presence Text

You can customize most of the presence text using `preferences.json`. Open this file with any text editor (e.g., Notepad, Notepad++, etc.) and modify as desired, although it is recommended to use the built-in application interface.

#### Available Patterns

These patterns can be used to dynamically update the presence text. They get updated every 15 seconds, whether you switch rooms or change YNO games. Just be sure you're not misspelling anything in case it doesn't seem to work well.

- **$gametype**: The YNO game you're currently playing, e.g., Unconscious Online, Yume 2kki, etc.
- **$location**: Your current location in the game, e.g., Urotsuki's Room, The Nexus, etc. Defaults to "Unknown Location" if no location is available or unknown.
- **$playersonline**: The total number of players currently playing the game.
- **$playersonmap**: The number of players in the current map.
- **$version**: The current application version.

### Important Note

Due to pypresence error handling, if you need to leave an entry empty (for example, the presence state message), insert at least three whitespace characters, like this: `"   "` (notice the blank spaces). Leaving entries fully empty will result in a warning, and your presence won't be updated.

## KnownProblems

1. The installation process may be too complex for less technologically inclined users, requiring multiple steps/configurations;
2. The application interface is not interesting enough and lacks visual effort.

## Contributions

Feel free to open issues and submit pull requests.

## License

This project is licensed under the GPL license. You are free to copy, redistribute, modify, or otherwise use this software as you wish.
