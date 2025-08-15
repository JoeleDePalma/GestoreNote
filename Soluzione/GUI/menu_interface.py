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
import json

images_path = Path(__file__).parent / "images"
credentials_path = Path(__file__).parent.parent / "credentials.json"

class menu_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        self.setFixedSize(800, 600)
        
        # Initialization variables

        self.toolbar_list = []
        self.tools_notes_list = []
        self.night_mode_on = False

        # Commons styles

        self.tools_style = """
            QPushButton
            {{
                border-radius: 15px;
                margin-left: -15px;
                background-color: {normal_background_color};
                border: 1px solid {normal_border_color};
                color: {normal_text_color};
            }}

            QPushButton:hover
            {{
                border-radius: 15px;
                margin-left: -15px;
                background-color: {hover_background_color};
                border: 1px solid {hover_border_color};
                color: {hover_text_color};
            }}

            QPushButton:pressed
            {{
                border-radius: 15px;
                margin-left: -15px;
                background-color: {pressed_background_color}; 
                border: 1px solid {pressed_border_color};
                color: {pressed_text_color};
            }}

                        """


        # Input camps and texts initialization
        
        with open(credentials_path, "r") as file:
            credentials = json.load(file)

        
        self.profile_button = QPushButton(QIcon(str(images_path / "profile_image.png")), f"  {credentials["username"]}" if len(credentials["username"]) < 8 else f"{credentials["username"][:8]}...")

        self.toolbar_notes_button = QPushButton(QIcon(str(images_path / "notes_icon.png")), "Appunti")
        self.toolbar_list.append(self.toolbar_notes_button)

        self.toolbar_settings_button = QPushButton(QIcon(str(images_path / "settings_icon.png")), "Impostazioni")
        self.toolbar_list.append(self.toolbar_settings_button)

        self.toolbar_nightmode_button = QPushButton("🌙 Modalità Notte")
        self.toolbar_list.append(self.toolbar_nightmode_button)

        self.toolbar_notes_show = QPushButton(QIcon(str(images_path / "clipboard_icon.png")), "Mostra")
        self.tools_notes_list.append(self.toolbar_notes_show)

        self.toolbar_notes_save = QPushButton(QIcon(str(images_path / "save_icon.png")),"Salva")
        self.tools_notes_list.append(self.toolbar_notes_save)

        self.toolbar_notes_delete = QPushButton(QIcon(str(images_path / "delete_icon.png")),"Elimina")
        self.tools_notes_list.append(self.toolbar_notes_delete)
        

        # Input camps and text modellation

        self.toolbar_nightmode_button.clicked.connect(self.night_mode)

        self.toolbar_notes_button.clicked.connect(self.tools_notes_show)

        self.profile_button.setFixedSize(140, 30)
        self.profile_button.setIconSize(QSize(20, 20))
        self.profile_button.setStyleSheet(self.tools_style.format(
            normal_text_color="black",
            normal_border_color="black",
            normal_background_color="white",
            hover_text_color="black",
            hover_border_color="black",
            hover_background_color="#F7F7F7",
            pressed_text_color="black",
            pressed_border_color="black",
            pressed_background_color="#F3F3F3"
        ))
        self.profile_button.clicked.connect(self.toolbar_appear)

        # IMPORTANT: Tools styles are in "toolbar layout" section
        

        # layout initialization

        self.layout = QVBoxLayout()

        # toolbar layout
        
        self.toolbar_layout = QVBoxLayout()

        self.set_tools(lenght = 120, style = dict(
                     
                normal_text_color = "black",
                normal_border_color = "black",
                normal_background_color = "white",

                hover_text_color = "black",
                hover_border_color = "black",
                hover_background_color = "#F7F7F7",

                pressed_text_color = "black",
                pressed_border_color = "black",
                pressed_background_color = "#F3F3F3"
                                                   
                                              ))
        
        self.toolbar_layout.setAlignment(Qt.AlignTop)


        # layout configuration

        self.layout.addWidget(self.profile_button)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.toolbar_layout)
        self.setLayout(self.layout)



    def toolbar_appear(self):
        is_visible = self.toolbar_notes_button.isVisible()
        for i in self.toolbar_list:
            i.setVisible(not is_visible)
        
        for tool in self.tools_notes_list:
            tool.setVisible(False)


    def set_tools(self, lenght, style):
        for i in self.toolbar_list:
            
            i.setFixedSize(lenght, 30)
            i.setIconSize(QSize(30, 30))
            i.setVisible(False)
            i.setStyleSheet(self.tools_style.format(**style))
            self.toolbar_layout.addWidget(i)

            if i == self.toolbar_notes_button:
                
                for tool in self.tools_notes_list:
                    tool.setFixedSize(lenght-20, 30)
                    tool.setIconSize(QSize(20, 20))
                    tool.setVisible(False)
                    tool.setStyleSheet(self.tools_style.format(**style))
                    self.toolbar_layout.addWidget(tool)



    def night_mode(self):
        self.night_mode_on = not self.night_mode_on
        
        if self.night_mode_on:

            style = dict(
            
            normal_text_color = "white",
            normal_border_color = "#5A5A5C",
            normal_background_color = "#3A3A3C",
            
            hover_text_color = "white",
            hover_border_color = "#5A5A5C",
            hover_background_color = "#505052",

            pressed_text_color = "white",
            pressed_border_color = "#5A5A5C",
            pressed_background_color = "#2C2C2E"

                        )
            self.set_tools(120, style = style)
            self.profile_button.setStyleSheet(self.tools_style.format(**style))
            self.setStyleSheet("background-color: #1C1C1E")
            

        else:

            style = dict(
            
            normal_text_color = "black",
            normal_border_color = "black",
            normal_background_color = "white",

            hover_text_color = "black",
            hover_border_color = "black",
            hover_background_color = "#F7F7F7",

            pressed_text_color = "black",
            pressed_border_color = "black",
            pressed_background_color = "#F3F3F3"
            
                        )
            self.set_tools(120, style = style)
            self.profile_button.setStyleSheet(self.tools_style.format(**style))   
            self.setStyleSheet("background-color: white")

        
    def tools_notes_show(self):
        is_visible = self.toolbar_notes_show.isVisible()
        for i in self.tools_notes_list:
            i.setVisible(not is_visible)
        
