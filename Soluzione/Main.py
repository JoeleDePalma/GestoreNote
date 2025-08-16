# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
import logging

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
def main():
    
    # create the application instance
    app = QApplication(sys.argv)

    from GUI.menu_interface import menu_window
    window = menu_window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()