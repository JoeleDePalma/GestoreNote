from pathlib import Path
import importlib.util

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)

from PySide6.QtWidgets import QApplication, QLineEdit, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class create_notes_window(QWidget):
    def __init__(self, username, public_cryptography, private_cryptography, account_verified, night_mode_on):
        super().__init__()
        self.username = username
        self.public_cryptography = public_cryptography
        self.private_cryptography = private_cryptography
        self.account_verified = account_verified
        self.night_mode_on = night_mode_on

        images_dir = Path(__file__).parent / "Images"

        # Window initialization
        self.setWindowTitle("Crea note")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #f2f2f2;")

        # Input camps and texts initialization
        self.note_title_input_box = QLineEdit()
        self.save_public_button = QPushButton("Salva nota pubblica")
        self.save_private_button = QPushButton("Salva nota privata")
        self.goback_menu = QPushButton(QIcon(str( images_dir / "goback_icon.png")), "Indietro")

        # Commons styles

        self.buttons_style = """
        
            QPushButton 
            {{
                background-color: #007BFF;  
                color: white;  
                border: 1px solid {border_color};  
                border-radius: 10px; 
                font-family: Arial;
                font-size: 16px;
            }}

            QPushButton:hover
            {{
                background-color: #006FE6;
            }}
        
            QPushButton:pressed
            {{
                background-color: #0062CC;
            }}

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

        self.tools_style_night = dict(
                     
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

        
        # Input camps and texts modellation

        self.note_title_input_box.setPlaceholderText("Titolo della nota")
        self.note_title_input_box.setFixedSize(350, 60)
        self.save_private_button.setFixedSize(175, 40)
        
        self.save_private_button.clicked.connect(lambda: self.create_notes(f"{self.note_title_input_box.text().strip()}.txt", public=False))

        self.save_public_button.setFixedSize(175, 40)
        self.save_public_button.clicked.connect(lambda: self.create_notes(f"{self.note_title_input_box.text().strip()}.txt", public=True))

        self.goback_menu.setFixedSize(150, 30)
        self.goback_menu.clicked.connect(self.exit)

        if not self.night_mode_on:
            
            self.setStyleSheet("background-color: #f2f2f2")

            self.goback_menu.setStyleSheet(self.tools_style.format(**self.tools_style_day))

            self.save_private_button.setStyleSheet(self.buttons_style.format(border_color = "black"))

            self.save_public_button.setStyleSheet(self.buttons_style.format(border_color = "black"))

            self.note_title_input_box.setStyleSheet("""
        
                            background-color: white; 
                            font-size: 16px;
                            font-family: Arial;
                            border: 1px solid #ccc;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            color: black;
        
                            
                                                """)

        else:

            self.setStyleSheet("background-color: #1C1C1E")

            self.goback_menu.setStyleSheet(self.tools_style.format(**self.tools_style_night))

            self.save_private_button.setStyleSheet(self.buttons_style.format(border_color = "white"))

            self.save_public_button.setStyleSheet(self.buttons_style.format(border_color = "white"))

            self.note_title_input_box.setStyleSheet("""
        
                            background-color: #3A3A3C; 
                            font-size: 16px;
                            font-family: Arial;
                            border: 1px solid #5A5A5C;
                            border-radius: 20px;
                            margin-bottom: 20px;
                            color: white;
        
                            
                                                """)

        # Layout Initialization
        self.layout = QVBoxLayout()

        # Tools layout configuration
        self.tools_layout = QHBoxLayout()
        self.tools_layout.addWidget(self.goback_menu)
        self.tools_layout.setContentsMargins(0, 10, 0, 0)
        self.tools_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Buttons layout configuration
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.save_public_button)
        self.buttons_layout.addWidget(self.save_private_button)

        # main layout configuration
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.note_title_input_box)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.setContentsMargins(0, 50, 0, 0)
        self.main_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # Layout configuration
        self.layout.addLayout(self.tools_layout)
        self.layout.addLayout(self.main_layout)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)


    def create_notes(self, notes_name, public):
        if public:
            file = functions.FileNotes(Path(__file__).parent.parent / self.username / "notes" / "public" / notes_name)
            created = file.create()

        else: 
            file = functions.FileNotes(Path(__file__).parent.parent / self.username / "notes" / "private" / notes_name)
            created = file.create()

        if created:
            from GUI.menu_interface import menu_window
            win_menu = menu_window(
                self.username, 
                public_cryptography = self.public_cryptography, 
                private_cryptography = self.private_cryptography, 
                account_verified = self.account_verified,
                night_mode_on = self.night_mode_on
                )
            win_menu.show()
            self.close()

        else:
            error_label = QLabel("Errore durante la creazione della nota.")
            error_label.setStyleSheet("color: red; font-size: 16px;")
            self.layout.addWidget(error_label)
            self.layout.setAlignment(Qt.AlignCenter)


    def exit(self):
        from GUI.menu_interface import menu_window
        win_menu = menu_window(
            username=self.username,
            public_cryptography=self.public_cryptography,
            private_cryptography=self.private_cryptography,
            account_verified=self.account_verified,
            night_mode_on=self.night_mode_on
        )
        win_menu.show()
        self.close()