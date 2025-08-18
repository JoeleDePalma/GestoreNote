# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication

# credentials file path
def main():
    
    # create the application instance
    app = QApplication([])
    
    from GUI.signin_interface import signin_window

    window = signin_window()
    window.show()
    app.exec()


if __name__ == "__main__":
    main() 