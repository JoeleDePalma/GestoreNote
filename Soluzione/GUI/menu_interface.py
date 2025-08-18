# -*- coding: utf-8 -*-


from pathlib import Path
import importlib.util
from venv import create

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)

from PySide6.QtWidgets import QApplication, QToolBar, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint
from PySide6.QtGui import QIcon
import sqlite3
import os

conn = sqlite3.connect(Path(__file__).parent.parent / "credentials.db")
cursor = conn.cursor()

images_path = Path(__file__).parent / "images"

class menu_window(QWidget):
    
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle("Menu")
        self.setFixedSize(800, 600)
        
        # Initialization variables

        self.toolbar_list = []
        self.tools_notes_list = []
        self.tools_settings_list = []
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


        self.notes_style = """
            QPushButton
            {{
                border-radius: 15px;
                margin-right: {margin};
                background-color: {normal_background_color};
                border: 1px solid {normal_border_color};
                color: {normal_text_color};
            }}

            QPushButton:hover
            {{
                border-radius: 15px;
                margin-right {margin};
                background-color: {hover_background_color};
                border: 1px solid {hover_border_color};
                color: {hover_text_color};
            }}

            QPushButton:pressed
            {{
                border-radius: 15px;
                margin-right: {margin};
                background-color: {pressed_background_color}; 
                border: 1px solid {pressed_border_color};
                color: {pressed_text_color};
            }}

                        """


        self.notes_style_day = dict(
                     
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


        # Input camps and texts initialization
        
        cursor.execute("SELECT publ_pass FROM users WHERE username = ?", (self.username,))
        #self.publ_pass = cursor.fetchone()[0]
        
        
        self.profile_button = QPushButton(QIcon(str(images_path / "profile_image.png")), f"  {self.username if len(self.username) < 8 else f'{self.username[:8]}...'}")

        self.toolbar_notes_button = QPushButton(QIcon(str(images_path / "notes_icon.png")), "Appunti")
        self.toolbar_list.append(self.toolbar_notes_button)

        self.toolbar_settings_button = QPushButton(QIcon(str(images_path / "settings_icon.png")), "Impostazioni")
        self.toolbar_list.append(self.toolbar_settings_button)

        self.toolbar_nightmode_button = QPushButton("🌙 Modalità notte")
        self.toolbar_list.append(self.toolbar_nightmode_button)

        self.toolbar_notes_show = QPushButton(QIcon(str(images_path / "clipboard_icon.png")), "Mostra")
        self.tools_notes_list.append(self.toolbar_notes_show)

        self.toolbar_notes_create = QPushButton(QIcon(str(images_path / "create_icon.png")), "Crea")
        self.tools_notes_list.append(self.toolbar_notes_create)

        self.toolbar_notes_rename = QPushButton(QIcon(str(images_path / "rename_icon.png")), "Rinomina")
        self.tools_notes_list.append(self.toolbar_notes_rename)

        self.toolbar_notes_save = QPushButton(QIcon(str(images_path / "save_icon.png")),"Salva")
        self.tools_notes_list.append(self.toolbar_notes_save)

        self.toolbar_notes_delete = QPushButton(QIcon(str(images_path / "delete_icon.png")),"Elimina")
        self.tools_notes_list.append(self.toolbar_notes_delete)

        self.toolbar_close_button = QPushButton("❌ Chiudi")
        self.toolbar_list.append(self.toolbar_close_button)

        self.toolbar_settings_exit = QPushButton(QIcon(str(images_path / "exit_icon.jpg")), "Esci")
        self.tools_settings_list.append(self.toolbar_settings_exit)

        # Input camps and text modellation

        self.toolbar_nightmode_button.clicked.connect(self.night_mode)

        self.toolbar_settings_button.clicked.connect(self.tools_settings_show)

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

        self.toolbar_close_button.clicked.connect(self.close_app)

        self.toolbar_notes_show.clicked.connect(self.notes_appear)

        self.toolbar_notes_create.clicked.connect(self.create_notes_func)

        self.toolbar_settings_exit.clicked.connect(self.exit)

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
        self.toolbar_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Notes layout
        self.notes_directory = Path(__file__).parent.parent / self.username / "notes"
        self.public_notes = os.listdir(self.notes_directory/"public")
        self.private_notes = os.listdir(self.notes_directory/"private")
        self.sep_notes_list = [self.public_notes, self.private_notes]
        self.notes_buttons = [[], []]

        self.notes_layout = QVBoxLayout()

        self.set_notes(style = self.notes_style_day)

        self.notes_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)


        # main layout configuration

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.toolbar_layout)
        self.main_layout.addLayout(self.notes_layout)

        # layout configuration

        self.layout.addWidget(self.profile_button)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.main_layout)
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

            if i == self.toolbar_settings_button:

                for tool in self.tools_settings_list:
                    tool.setFixedSize(lenght-20, 30)
                    tool.setIconSize(QSize(20, 20))
                    tool.setVisible(False)
                    tool.setStyleSheet(self.tools_style.format(**style))
                    self.toolbar_layout.addWidget(tool)


    def set_notes(self, style, visible=False):
        def visibility(buttons_list):
            is_visible = buttons_list[0].isVisible() if buttons_list else False
            for button in buttons_list:
                button.setVisible(not is_visible)

        for i, notes in enumerate(self.sep_notes_list): 
            if i == 0:
                style["margin"] = "-15px"
                self.public_notes_button = QPushButton("Appunti pubblici")
                self.public_notes_button.setFixedSize(160, 30)
                self.public_notes_button.setVisible(visible)
                self.public_notes_button.setStyleSheet(self.notes_style.format(**style))
                self.public_notes_button.clicked.connect(lambda: visibility(self.notes_buttons[0]))
                self.notes_layout.addWidget(self.public_notes_button)
                style["margin"] = "0px"
                for j in notes:
                    if j.endswith(".txt"):
                        if len(j[:-4]) < 20:
                            button = QPushButton(j[:-4])
                        else:
                            button = QPushButton(f"{j[:-4][:10]}...")
                        button.setFixedSize(160, 30)
                        button.setStyleSheet(self.notes_style.format(**style))
                        button.setVisible(visible)
                        self.notes_buttons[0].append(button)
                        self.notes_layout.addWidget(button)

            if i == 1:
                style["margin"] = "-15px"
                self.private_notes_button = QPushButton("Appunti privati")
                self.private_notes_button.setFixedSize(160, 30)
                self.private_notes_button.setVisible(visible)
                self.private_notes_button.setStyleSheet(self.notes_style.format(**style))
                self.private_notes_button.clicked.connect(lambda: visibility(self.notes_buttons[1]))
                self.notes_layout.addWidget(self.private_notes_button)
                style["margin"] = "0px"
                for j in notes:
                    if j.endswith(".txt"):
                        if len(j[:-4]) < 20:
                            button = QPushButton(j[:-4])
                        else:
                            button = QPushButton(f"{j[:-4][:10]}...")
                        button.setFixedSize(160, 30)
                        button.setStyleSheet(self.notes_style.format(**style))
                        button.setVisible(visible)
                        self.notes_buttons[1].append(button)
                        self.notes_layout.addWidget(button)


    def notes_appear(self, hide = False):
        if not hide:
            if self.public_notes_button.isVisible():
                self.public_notes_button.setVisible(False)
                self.private_notes_button.setVisible(False)
            
                for button in self.notes_buttons[0]: button.setVisible(False)
                for button in self.notes_buttons[1]: button.setVisible(False)
                self.toolbar_notes_show.setText("Mostra")

            else:
                self.public_notes_button.setVisible(True)
                self.private_notes_button.setVisible(True)
                self.toolbar_notes_show.setText("Nascondi")

        else:
            self.public_notes_button.setVisible(False)
            self.private_notes_button.setVisible(False)
            
            for button in self.notes_buttons[0]: button.setVisible(False)
            for button in self.notes_buttons[1]: button.setVisible(False)


    def create_notes_func(self):
        from GUI.create_notes_interface import create_notes_window
        win_create = create_notes_window(self.username)
        win_create.show()
        self.close()

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

            self.toolbar_nightmode_button.setText("🌞 Modalità giorno")

            self.set_tools(120, style = style)

            style["margin"] = "-15px"
            self.public_notes_button.setStyleSheet(self.notes_style.format(**style))
            self.private_notes_button.setStyleSheet(self.notes_style.format(**style))
            
            style["margin"] = "0px"
            for i in range(2):
                for j in self.notes_buttons[i]:
                    j.setStyleSheet(self.notes_style.format(**style))
            self.notes_appear(hide = True)

            style.pop("margin")

            self.toolbar_notes_show.setText("Mostra")

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

            self.toolbar_nightmode_button.setText("🌙 Modalità notte")

            self.set_tools(120, style = style)

            style["margin"] = "-15px"
            self.public_notes_button.setStyleSheet(self.notes_style.format(**style))
            self.private_notes_button.setStyleSheet(self.notes_style.format(**style))
            
            style["margin"] = "0px"
            for i in range(2):
                for j in self.notes_buttons[i]:
                    j.setStyleSheet(self.notes_style.format(**style))
            self.notes_appear(hide = True)
            
            style.pop("margin")

            self.toolbar_notes_show.setText("Mostra")

            self.profile_button.setStyleSheet(self.tools_style.format(**style))   
            
            self.setStyleSheet("background-color: white")
    
    
    def exit(self):
        from GUI.signin_interface import signin_window
        win_signin = signin_window()
        win_signin.show()
        self.close()

    def tools_settings_show(self):
        is_visible = self.tools_settings_list[0].isVisible()
        for i in self.tools_settings_list:
            i.setVisible(not is_visible)

    def tools_notes_show(self):
        is_visible = self.toolbar_notes_show.isVisible()
        for i in self.tools_notes_list:
            i.setVisible(not is_visible)

    def close_app(self):
        self.close()
        cursor.close()
        conn.close()
