from pathlib import Path
import importlib.util

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)

import os

from PySide6.QtWidgets import QApplication, QTextEdit, QLineEdit, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class rename_notes_window(QWidget):
    def __init__(self, username, public_cryptography, private_cryptography, account_verified, title, state):
        super().__init__()
        self.username = username
        self.public_cryptography = public_cryptography
        self.private_cryptography = private_cryptography
        self.account_verified = account_verified
        self.state = state
        self.title = title

        self.notes_dir = Path(__file__).parent.parent / self.username / "notes" / self.state 
        self.images_dir = Path(__file__).parent / "images" 

        # Window initialization
        self.setWindowTitle("Rinomina note")
        self.setFixedSize(400, 250)

        # Input camps and texts initialization
        self.goback_menu = QPushButton(QIcon(str(self.images_dir / "goback_icon.png")), "Indietro")
        self.note_title_input_box = QLineEdit()
        self.rename_button = QPushButton("Rinomina")

        # Commons styles

        self.rename_style = """
        
            QPushButton 
            {
                background-color: #007BFF;  
                color: white;  
                border: none;  
                border-radius: 20px; 
                font-family: Arial;
                font-size: 16px;
            }

            QPushButton:hover
            {
                background-color: #006FE6;
            }
        
            QPushButton:pressed
            {
                background-color: #0062CC;
            }

                                  """

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

        self.tools_style_day = dict(
                     
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
        

        # Input camps and texts modellation


        self.note_title_input_box.setStyleSheet("""
        
                            background-color: white; 
                            font-size: 16px;
                            font-family: Arial;
                            border: 1px solid #ccc;
                            border-radius: 10px;
        
                            
                                                """)
        self.note_title_input_box.setFixedSize(350, 40)
        self.note_title_input_box.setText(title[:-4])

        self.rename_button.setFixedSize(350, 45)
        self.rename_button.setStyleSheet(self.rename_style)
        self.rename_button.clicked.connect(self.rename_func)

        self.goback_menu.setFixedSize(150, 30)
        self.goback_menu.setStyleSheet(self.tools_style.format(**self.tools_style_day))
        self.goback_menu.clicked.connect(self.goback_menu_func)


        # Layout Initialization

        self.layout = QVBoxLayout()

        # Tools layout  configuration 

        self.tools_layout = QHBoxLayout()
        self.tools_layout.addWidget(self.goback_menu)
        self.tools_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Rename layout configuration

        self.rename_layout = QVBoxLayout()
        
        self.rename_layout.addWidget(self.note_title_input_box)
        self.rename_layout.addWidget(self.rename_button)
        self.rename_layout.setContentsMargins(0, 45, 0, 0)
        self.rename_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Layout configuration
        self.layout.addLayout(self.tools_layout)
        self.layout.addLayout(self.rename_layout)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


    def rename_func(self):
        new_title = self.note_title_input_box.text().strip()
        os.rename(self.notes_dir / self.title, self.notes_dir / f"{new_title}.txt")
        from GUI.menu_interface import menu_window
        menu_win = menu_window(username = self.username, public_cryptography = self.public_cryptography, private_cryptography = self.private_cryptography, account_verified = self.account_verified)
        menu_win.show()
        self.close()


    def goback_menu_func(self):
        from GUI.menu_interface import menu_window
        menu_win = menu_window(username = self.username, public_cryptography = self.public_cryptography, private_cryptography = self.private_cryptography, account_verified = self.account_verified)
        menu_win.show()
        self.close()
        
