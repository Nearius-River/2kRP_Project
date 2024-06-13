# 2kRP Project

https://ynoproject.net

This project aims to integrate Discord Rich Presence with YNO games for the navigator, while (hopefully) being lightweight, easy to use and to customize.

It utilizes a browser extension to act as a "linker", whose primary function is to send site data (such as location, player count, current game, etc) to the running Python application on the user's system through a localhost connection.

Most of the data the extension gathers is captured from HTML elements of the site itself.

<div align="center">
    <img src="https://github.com/Nearius-River/2kRP_Project/assets/49107257/d3bdd888-5fb3-43d9-9bba-56c5f0c266f7" alt="Example of how presence looks.">
</div>

## Project Structure

- `2kRP_Extension/`: Contains the browser extension files.
- `2kRP_Presence/`: Contains the rich presence application. Also handles the local server communication with the extension.

## Installation

### Requisites

- Python 3.8+ with pip available;
- 2kRP extension available for the navigator;
- Discord desktop app installed and running (for updating the rich presence).

### Instructions

1. Download the project as the zip file and extract it (pasting the link will auto-download the latest zip):

    ```sh
    https://github.com/Nearius-River/2kRP_Project/archive/refs/heads/master.zip
    ```

2. Go to '2kRP_Presence' and install the dependecies:

    ```sh
    pip install -r requirements.txt
    ```

3. Run the app:

    ```sh
    python app.py
    ```

    Alternatively, you can double-click "app.py" to open it.

## Usage

- To start the server connection, open app.py and DO NOT close it (doing so will instantly terminate the server connection).
- If "Connection established!" appears in the terminal, you can go to the YNO site and pick a game to play. Your presence will be updated as long as the app is running.
- `preferences.json`: You can customize most of the presence text here. Open it with any text editor (Notepad, Notepad++, etc.) or using the application interface and modify it as desired. Note: some patterns can be used, such as $location or $playersonline. A complete description of the available patterns:
    - **$gametype**: The YNO game you're currently playing, e.g., Unconscious Online, Yume 2kki, etc.
    - **$location**: Where you are currently located in the game, e.g., Urotsuki's Room, The Nexus, etc. Defaults to "Unknown Location" if no location is available or unknown.
    - **$playersonline**: The total number of players currently playing the game.
    - **$playersonmap**: The number of players in the current map (the map you're in).
    - **$version**: The current application version.
    - These patterns can be used anywhere you like. They get updated every 15 seconds, whether you switch rooms or hop from one YNO game to another. Just be sure you're not misspelling anything in case it doesn't seem to work as intended.

## Known problems

~~The program uses a simple terminal interface to communicate with the user, only allowing minimizing or closing the window.~~

~~Proposed Solution: Implement a complete graphical interface with tabs for setting user preferences and configuring the app.~~

**Solved**, with the implementation of the basic GUI interface using tkinter. (That said, there's still much room for improvement!)

The installation process may be too complex for less technologically inclined users, requiring multiple steps/configurations.

Proposed Solution: Convert the app into a single executable (.exe) file while retaining functionality OR implement more user-friendly installation methods.

## Contributions

Feel free to open issues and submit pull requests.

## License

This project is licensed under the GPL license. You are free to copy, redistribute, modify, or otherwise use this software as you wish.
