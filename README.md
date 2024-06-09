# 2kRP Project

https://ynoproject.net/2kki/

This project aims to integrate Discord Rich Presence with Yume 2kki for the navigator, while (hopefully) being easy to use and customize.

It utilizes a browser extension to act as a "linker", whose primary function is to send site data (such as location and player count) to the running Python application on the user's system through a localhost connection.

Most of the data the extension gathers is captured from the HTML elements of the site itself.

<div align="center">
    <img src="https://github.com/Nearius-River/2kRP_Project/assets/49107257/d3bdd888-5fb3-43d9-9bba-56c5f0c266f7" alt="Example of how presence looks.">
</div>

## Project Structure

- `2kRP_Extension/`: Contains the browser extension files.
- `2kRP_Presence/`: Contains the rich presence application. Also handles the local server communication with the extension.

## Installation

**NOTE**: This section only covers the installation for the **Python application**. If you are a normal user, consider using the **packed executable file** instead. This is intended for development only, but you can also use it (and even compile your own executable with it if you feel like it).

### Requisites

- Python 3.x (with pip available)
- Discord (desktop app) installed for updating the Rich Presence (you must be logged in).

### Instructions

1. Download the project as the zip file and extract it (pasting the link will auto-download the latest zip):

    ```sh
    https://github.com/Nearius-River/2kRP_Project/archive/refs/heads/master.zip
    ```

2. Install the dependecies:

    ```sh
    pip install -r requirements.txt
    ```

3. Open the `.env.example` file and configure it with your client ID:

    ```sh
    # Insert with actual ID:
    CLIENT_ID="102482759437"
    ```

4. Run the app:

    ```sh
    python app.py
    ```

    Alternatively, you can double-click "app.py" to open it.

## Usage

- To start the server connection, open app.py and DO NOT close it (doing so will instantly terminate the server connection).
- If "Connection established!" appears in the terminal, you can go to the Yume 2kki site and start playing. Your presence will be updated as long as the app is running.
- `preferences.json`: You can customize most of the presence text here. Open it with any text editor (Notepad, Notepad++, etc.) and modify it as desired. Note: some patterns can be used, such as $location or $playersonline. A complete description of the available patterns:

    `$location`: Where you are currently located in the game, e.g., Urotsuki's Room, The Nexus, etc. Defaults to "Unknown Location" if no location is available or unknown.

    `$playersonline`: The total number of players currently playing the game.

    `$playersonmap`: The number of players in the current map (the map you're in).

    `$version`: The current application version.

These patterns can be used anywhere you like.

## Known problems

~~1. The program uses a simple terminal interface to communicate with the user, only allowing minimizing or closing the window.~~

~~Proposed Solution: Implement a complete graphical interface with tabs for setting user preferences and configuring the app.~~

**Update**: "Solved", with the implementation of the basic GUI interface using tkinter. Though, still needs a BIG visual update before it can be fully considered solved.

~~2. The installation process may be too complex for less technologically inclined users, requiring multiple steps/configurations.~~

~~Proposed Solution: Convert the app into a single executable (.exe) file while retaining functionality OR implement more user-friendly installation methods.~~

**Update**: Went with first option, using pyinstaller to help with the generation of a .exe file for the app.

## Contributions

Feel free to open issues and submit pull requests.

## License

This project is licensed under the GPL license. You are free to copy, redistribute, modify, or otherwise use this software as you wish.