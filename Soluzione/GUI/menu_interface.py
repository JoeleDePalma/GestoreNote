# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt, QSize
from PySide6.QtGui import QIcon
from login_interface import login_window
from signin_interface import signin_window

class menu_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")































app = QApplication([])
window = menu_window()
window.show()
app.exec()