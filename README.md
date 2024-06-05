# 2kRP Project

This project intends to add Discord Rich Presence compatibility for Yume 2kki on the navigator (not the desktop application).
It utilizes a browser extension to act as a "linker", sending necessary data to a receiver app in the desktop through a localhost connection. The presence is then updated for the connected client using pypresence.

## Project Structure

- `2kRP_Extension/`: Contains the browser extension files.
- `2kRP_Presence/`: Contains the rich presence application. Also responsible for the local server.

## Installation

### Requisites

- Python 3.x
- Discord (desktop app) installed for updating the Rich Presence (you must be logged in).

### Instructions

1. Download the project as a zip and extract (simply pasting the link will auto-download the latest zip):

    ```sh
    https://github.com/Nearius-River/2kRP_Project/archive/refs/heads/master.zip
    ```

2. Install the dependecies:

    ```sh
    pip install -r requirements.txt
    ```

3. Open the `.env` file and configure with your client id.

4. Run the app:

    ```sh
    python app.py
    ```

    You can also double click "app.py" to open normally.

## Usage

- To start the server connection, open app.py and DO NOT close it (doing so will instantly terminate the server connection)
- If you see "Connection established!" in the terminal, you can go to Yume 2kki site and start playing. Your presence will be updated as long as the app is running.

## Known problems

1. The program uses a simple terminal interface to communicate with the user, giving only the option of minimizing or closing the window.
Proposed solution: Implement a complete graphical interface

2. The installation may be too hard for lesser technological people and requires too many steps/configurations to be made
Proposed solution: Transform the app into a singular .exe file keeping the functionality OR implement better ways to install the app automatically.

## Contributions

Feel free to open issues and send pull requests.

## Licença

This project is licensed under a GPL license. Feel free to copy, redistribute, modify or otherwise do whatever you want with this software.
