# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# Add the parent directory of this file to the system path
sys.path.append(str(Path(__file__).parent))

from functions import *
from GUI.signin_interface import *
from GUI.login_interface import *
import logging

logs_file_path = Path(__file__).parent / "file_logs.txt"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(directory_logs / "file_logs.txt"),
    filemode="a"
)

# Path to credentials file
credentials_path = Path(__file__).parent / "credentials.json"

# Create credentials.json if it does not exist or is empty
if not credentials_path.exists():
    credentials_path.write_text("{}")
    logging.info("File credentials.json created successfully.")
else:
    if credentials_path.stat().st_size == 0:
        credentials_path.write_text("{}")
        logging.info("File credentials.json existed but was empty, filled with '{}'.")

def main():
    with open(credentials_path, "r") as file:
        credentials = file.read()
        if not credentials.strip():
            logging.info("File credentials.json is empty, filling with '{}'.")
        else:
            logging.info("File credentials.json read successfully.")

    app = QApplication([])
    window = signin_window()
    window.show()
    app.exec()
        

if __name__== "__main__":
    main()



