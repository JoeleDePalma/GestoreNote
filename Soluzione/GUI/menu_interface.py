# -*- coding: utf-8 -*-


from pathlib import Path
import importlib.util

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)

from PySide6.QtWidgets import QApplication, QToolBar, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt, QSize, QPropertyAnimation, QPoint
from PySide6.QtGui import QIcon
from login_interface import login_window
from signin_interface import signin_window
import json

images_path = Path(__file__).parent / "images"
credentails_path = Path(__file__).parent.parent / "credentials.json"

class menu_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        self.setFixedSize(800, 600)
        
        # Initialization variables

        self.tools_list = []
        self.night_mode_on = False

        # Input camps and texts initialization

        with open(credentails_path, "r") as file:
            credentials = json.load(file)

        self.toolbar_button = QPushButton(QIcon(str(images_path / "profile_image.png")), f"  {credentials.get('username')}" if len(credentials.get("username"))<8 else f"{credentials.get("username")[:8]}...")

        self.toolbar_notes_button = QPushButton(QIcon(str(images_path / "notes_icon.png")), "Appunti")
        self.tools_list.append(self.toolbar_notes_button)

        self.toolbar_settings_button = QPushButton(QIcon(str(images_path/"settings_icon.png")), "Impostazioni")
        self.tools_list.append(self.toolbar_settings_button)

        self.toolbar_nightmode_button = QPushButton("🌙 Modalità Notte")
        self.toolbar_nightmode_button.clicked.connect(self.night_mode)
        self.tools_list.append(self.toolbar_nightmode_button)

        # Commons styles

        self.tools_style = """
            QPushButton
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: white;
                border: 1px solid black;
                color: black;
            }

            QPushButton:hover
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #F7F7F7;
                border: 1px solid black;
                color: black;
            }

            QPushButton:pressed
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #F3F3F3; 
                border: 1px solid black;
                color: black;
            }

                        """

        # Input camps and text modellation

        self.toolbar_button.setFixedSize(140, 30)
        self.toolbar_button.setIconSize(QSize(20, 20))
        self.toolbar_button.clicked.connect(self.toolbar_appear)
        self.toolbar_button.setStyleSheet(self.tools_style)

        # IMPORTANT: Tools styles are in "toolbar layout" section
        

        # layout initialization

        layout = QVBoxLayout(self)


        # toolbar layout

        self.toolbar_layout = QVBoxLayout()

        self.set_tools()
        
        self.toolbar_layout.setAlignment(Qt.AlignTop)


        # layout configuration

        layout.addWidget(self.toolbar_button)
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(self.toolbar_layout)

    def toolbar_appear(self):
        is_visible = self.toolbar_notes_button.isVisible()
        for i in self.tools_list:
            i.setVisible(not is_visible)

    def set_tools(self):
        for i in self.tools_list:
            i.setFixedSize(120, 30)
            i.setIconSize(QSize(30, 30))
            i.setVisible(True)
            i.setStyleSheet(self.tools_style)
            self.toolbar_layout.addWidget(i)

    def night_mode(self):
        self.night_mode_on = not self.night_mode_on
        
        if not self.night_mode_on:
            
            self.tools_style = """
            QPushButton
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: white;
                border: 1px solid black;
                color: black;
            }

            QPushButton:hover
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #F7F7F7;
                border: 1px solid black;
                color: black;
            }

            QPushButton:pressed
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #F3F3F3; 
                border: 1px solid black;
                color: black;
            }

                        """

            self.set_tools()
            self.toolbar_button.setStyleSheet(self.tools_style)

        else:
            
            self.tools_style = """
            QPushButton
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #030303;
                border: 1px solid white;
                color: white;
            }

            QPushButton:hover
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #121212;
                border: 1px solid white;
                color: white;
            }

            QPushButton:pressed
            {
                border-radius: 15px;
                margin-left: -15px;
                background-color: #1A1A1A; 
                border: 1px solid white;
                color: white;
            }

                        """
    
            self.set_tools()
            self.toolbar_button.setStyleSheet(self.tools_style)




















app = QApplication([])
window = menu_window()
window.show()
app.exec()