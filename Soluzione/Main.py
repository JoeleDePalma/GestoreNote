# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import os
from PySide6.QtWidgets import QApplication
import logging
import json

# logs directory
logs_file_path = Path(__file__).parent / "logs" /"file_logs.txt"

# logging configuring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(logs_file_path),
    filemode="a"
)

# credentials file path
credentials_path = Path(__file__).parent / "credentials.json"

def main():
    # creates the file if it doesn't exist
    if not credentials_path.exists():
        try:
            credentials_path.write_text("{}")
            logging.info("File credentials.json created successfully.")
        except Exception as e:
            logging.error(f"Failed to create credentials.json: {e}")
            sys.exit(1)

    # verify if the file is empty
    if credentials_path.stat().st_size == 0:
        try:
            credentials_path.write_text("{}")
            logging.info("File credentials.json existed but was empty, filled with '{}'.")
        except Exception as e:
            logging.error(f"Failed to write to credentials.json: {e}")
            sys.exit(1)

    # reads file's content
    try:
        with open(credentials_path, "r") as file:
            credentials = json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse credentials.json: {e}")
        sys.exit(1)

    # verify credentials
    user_verified = False
    if "username" in credentials and "password" in credentials:
        if credentials["username"] and credentials["password"]:
            user_verified = True
            logging.info("Credentials are valid.")
        else:
            logging.info("Credentials are empty.")
    else:
        logging.info("Credentials file does not contain required fields.")

    # create the application instance
    app = QApplication(sys.argv)

    # shows the appropriate window based on user verification
    if user_verified:
        from GUI.menu_interface import menu_window
        window = menu_window()
        window.show()
        app.exec()
    else:
        from GUI.signin_interface import signin_window
        window = signin_window()
        window.show()
        app.exec()
        # restart application
        restart_application()


def restart_application():
    """
    Funzione per riavviare l'applicazione.
    """
    logging.info("Restarting application...")
    python = sys.executable  # Python interpreter path
    os.execl(python, python, *sys.argv)  # Restart the program


if __name__ == "__main__":
    main()