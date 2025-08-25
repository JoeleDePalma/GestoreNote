# -*- coding: utf-8 -*-

import importlib.util
from pathlib import Path

# Module's path to load
functions_path = Path(__file__).parent.parent / "functions.py"

# Loads dynamic module from the specified path
spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)


from PySide6.QtWidgets import QApplication, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt, QSize
from PySide6.QtGui import QIcon
import re

images_path = Path(__file__).parent / "Images"


class signin_window(QWidget):

    def __init__(self, night_mode_on = False):
        super().__init__()

        # Variables initialization
        self.night_mode_on = night_mode_on

        self.private_cryptography = None
            
        self.valid_username = False
        self.valid_password = False
        self.valid_priv_pass = False
        self.hidden_password = True
        self.hidden_priv_pass = True

        # Window initialization
        self.setWindowTitle("Registrati")
        self.setFixedSize(500, 650)
        

        # Input camps and texts initialization
        self.welcome_text = QLabel("Benvenuto!")

        self.username_input_box = QLineEdit()

        self.username_warning = QLabel("Il nome utente deve essere lungo almeno 5 caratteri")
        
        self.password_input_box = QLineEdit()

        self.priv_pass_input_box = QLineEdit()

        self.password_hide_button = QPushButton("")

        self.priv_pass_hide_button = QPushButton("")

        self.password_warning = QLabel("Le password devono contenere almeno 8 caratteri, maiuscoli e minuscoli")

        self.characters_warning = QLabel("Le password devono contenere almeno un carattere speciale")

        self.same_password_warning = QLabel("Le password devono essere diverse")

        self.signin_button = QPushButton("Registrati")

        self.username_exists_warning = QLabel("Nome utente già esistente")

        self.signin_text = QLabel("Crea il tuo account")

        self.login_link = QPushButton("Sei già registrato? Accedi")

        
        # Commons styles
        self.username_password_css = """
                                    QLineEdit
                                    {{
                                        background-color: {background_color}; 
                                        font-size: 16px;
                                        font-family: Arial;
                                        border: 1px solid {border_color};
                                        border-radius: 12px;
                                        color: {text_color};
                                    }}
                                    """

        self.username_password_day = dict(
            
            background_color = "white",
            border_color = "#ccc",
            text_color = "black"

            )

        self.username_password_night = dict(
            
            background_color = "#3A3A3C",
            border_color = "#5A5A5C",
            text_color = "white"

            )

        self.warning_style_css = """
            
                                    QLineEdit
                                    {{
                                    background-color: {background_color}; 
                                    font-size: 16px;
                                    font-family: Arial;
                                    border: 1px solid red;
                                    border-radius: 12px;
                                    }}

                                """

        self.cansign_style_css = """
                
                                    QLineEdit
                                    {{
                                    background-color: {background_color}; 
                                    font-size: 16px;
                                    font-family: Arial;
                                    border: 1px solid green;
                                    border-radius: 12px;
                                    }}

                                """

        self.input_style_day = dict(
            
            background_color = "white",
            text_color = "black"
            
                            )

        self.input_style_night = dict(
            
            background_color= "#3A3A3C",
            text_color = "white"
            
                            )

        self.warning_text_css = """
                                
                                    font-family: Arial;
                                    font-size: 10px;
                                    color: red;
                                
                                """

        # Input camps and text modellation
        self.welcome_text.setAlignment(Qt.AlignCenter)
        
        self.username_input_box.setPlaceholderText("Nome utente")
        self.username_input_box.setFixedSize(350, 40)
        self.username_input_box.setStyleSheet(self.username_password_css)
        self.username_input_box.textChanged.connect(lambda text: self.changed_text_input(text.strip(), "username"))

        self.password_input_box.setPlaceholderText("Password")
        self.password_input_box.setFixedSize(350, 40)
        self.password_input_box.setStyleSheet(self.username_password_css)
        self.password_input_box.textChanged.connect(lambda text: self.changed_text_input(text.strip(), "password"))
        self.password_input_box.setEchoMode(QLineEdit.Password) # Hides the password input by defaultself.password_input_box.setPlaceholderText("Password")
        
        self.priv_pass_input_box.setPlaceholderText("Password per i file privati")
        self.priv_pass_input_box.setFixedSize(350, 40)
        self.priv_pass_input_box.setStyleSheet(self.username_password_css)
        self.priv_pass_input_box.textChanged.connect(lambda text: self.changed_text_input(text.strip(), "priv_pass"))
        self.priv_pass_input_box.setEchoMode(QLineEdit.Password) # Hides the password input by default
        
        self.login_link.setFlat(True)
        self.login_link.setFixedSize(160, 20)
        self.login_link.setCursor(Qt.PointingHandCursor)
        self.login_link.clicked.connect(self.login_window_show)
        self.login_link.setStyleSheet("""
            
            QPushButton 
            {
                font-family: Poppins semibold;
                font-size: 15px;
                background: transparent !important;  /* Forces transparent background */
                text-decoration: underline;
                color: #007BFF; 
                border: none !important;  /* Forces to remove any border */
                padding: 0 !important;  /* Removes padding */
            }

            QPushButton:hover 
            {
                color: #0056b3;  
                background: transparent !important; 
            }

            QPushButton:pressed 
            {
                color: #004085;
                background: transparent !important; 
            }

        """)

        self.signin_text.setAlignment(Qt.AlignCenter)
        

        self.signin_button.setFixedSize(350, 45)
        self.signin_button.setCursor(Qt.PointingHandCursor)
        self.signin_button.setEnabled(False)
        self.signin_button.setStyleSheet("""
        
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

        """)
        self.signin_button.clicked.connect(self.signin_clicked_func)

        self.username_warning.setStyleSheet(self.warning_text_css)
        self.username_warning.setVisible(False)

        self.password_warning.setStyleSheet(self.warning_text_css)
        self.password_warning.setVisible(False)

        self.characters_warning.setStyleSheet(self.warning_text_css)
        self.characters_warning.setVisible(False)

        self.same_password_warning.setStyleSheet(self.warning_text_css)
        self.same_password_warning.setVisible(False)

        self.password_hide_button.setFixedSize(40, 25)
        self.password_hide_button.setIconSize(QSize(30, 30))
        self.password_hide_button.setStyleSheet("""
        
                                                    background-color: transparent;
                                                    border: none;

                                                """)
        self.password_hide_button.setCursor(Qt.PointingHandCursor)
        self.password_hide_button.clicked.connect(lambda: self.hide_password_func(True))

        self.priv_pass_hide_button.setFixedSize(40, 25)
        self.priv_pass_hide_button.setIconSize(QSize(30, 30))
        self.priv_pass_hide_button.setStyleSheet("""
        
                                                    background-color: transparent;
                                                    border: none;

                                                """)
        self.priv_pass_hide_button.setCursor(Qt.PointingHandCursor)
        self.priv_pass_hide_button.clicked.connect(lambda: self.hide_password_func(public = False))

        self.username_exists_warning.setStyleSheet(self.warning_text_css)
        self.username_exists_warning.setVisible(False)

        
        if not self.night_mode_on:

            self.setStyleSheet("background-color: #f2f2f2;")

            self.welcome_text.setStyleSheet("""
            
                font-family: Montserrat;
                font-size: 30px;
                font-weight: bold;
                color: black;
        
                                            """)

            self.signin_text.setStyleSheet("""
            
                        font-family: Arial;
                        font-size: 15px;
                        color: grey;
                        margin-bottom: 50px;
        
                                            """)

            self.dir_eye_open = images_path / "eye_open_day.png"
            self.dir_eye_close = images_path / "eye_close_day.png"
            self.password_hide_button.setIcon(QIcon(str(self.dir_eye_close)))
            self.priv_pass_hide_button.setIcon(QIcon(str(self.dir_eye_close)))

            self.password_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))
            self.priv_pass_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))
            self.username_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))

        else:

            self.setStyleSheet("background-color: #1C1C1E;")

            self.welcome_text.setStyleSheet("""
            
                font-family: Montserrat;
                font-size: 30px;
                font-weight: bold;
                color: white;
        
                                            """)

            self.signin_text.setStyleSheet("""
            
                        font-family: Arial;
                        font-size: 15px;
                        color: grey;
                        margin-bottom: 50px;
        
                                            """)

            self.dir_eye_open = images_path / "eye_open_night.png"
            self.dir_eye_close = images_path / "eye_close_night.png"
            self.password_hide_button.setIcon(QIcon(str(self.dir_eye_close)))
            self.priv_pass_hide_button.setIcon(QIcon(str(self.dir_eye_close)))

            self.password_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))
            self.priv_pass_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))
            self.username_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))



        # Layout Initialization
        layout = QVBoxLayout()

        # Button's layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_link)
        button_layout.setAlignment(Qt.AlignCenter)

        # Password layout
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input_box)
        password_layout.addWidget(self.password_hide_button)

        # Private password layout
        priv_pass_layout = QHBoxLayout()
        priv_pass_layout.addWidget(self.priv_pass_input_box)
        priv_pass_layout.addWidget(self.priv_pass_hide_button)

        
        # layout configuration
        layout.addWidget(self.welcome_text)
        layout.addWidget(self.signin_text)
        layout.addWidget(self.username_input_box)
        layout.addWidget(self.username_exists_warning)
        layout.addWidget(self.username_warning)
        layout.addLayout(password_layout)
        layout.addLayout(priv_pass_layout)
        layout.addWidget(self.same_password_warning)
        layout.addWidget(self.password_warning)
        layout.addWidget(self.characters_warning)
        layout.addWidget(self.signin_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout) 
        
        layout.setContentsMargins(75, 0, 75, 100)
        self.setLayout(layout)


    # Connect the buttons to the functions

    def login_window_show(self):
        """
        Function to show the login window when the user clicks on the login link.
        """
        from GUI.login_interface import login_window
        self.login_win = login_window(self.night_mode_on)
        self.login_win.show()
        self.close()


    def hide_password_func(self, public = True):
        """
        Function to hide or show the password in the password input box when the user clicks on the eye button.
        """
        if public:
            self.hidden_password = not self.hidden_password  # Toggle the hidden password state

            if self.hidden_password: self.password_hide_button.setIcon(QIcon(str(self.dir_eye_close))); self.password_input_box.setEchoMode(QLineEdit.Password)
            else: self.password_hide_button.setIcon(QIcon(str(self.dir_eye_open))); self.password_input_box.setEchoMode(QLineEdit.Normal)

        else:
            self.hidden_priv_pass = not self.hidden_priv_pass  # Toggle the hidden password state

            if self.hidden_priv_pass: self.priv_pass_hide_button.setIcon(QIcon(str(self.dir_eye_close))); self.priv_pass_input_box.setEchoMode(QLineEdit.Password)
            else: self.priv_pass_hide_button.setIcon(QIcon(str(self.dir_eye_open))); self.priv_pass_input_box.setEchoMode(QLineEdit.Normal)


    def signin_clicked_func(self):
        """
        Function to call after the user clicks on the signin button.
        """
        # Reads the username and password input from the input boxes
        self.username_input = self.username_input_box.text().strip()
        self.password_input = self.password_input_box.text().strip()
        self.priv_pass_input = self.priv_pass_input_box.text().strip()

        account = functions.Account(username = self.username_input, password = self.password_input, priv_pass = self.priv_pass_input)
        self.verified_account, self.public_cryptography, self.private_cryptography = account.sign_in()

        if not self.verified_account:
            self.username_exists_warning.setVisible(True)
            if not self.night_mode_on: self.username_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
            else: self.username_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))
            return

        # Creates the directories
        directory_users = Path(__file__).parent.parent / "users"
        directory_all = directory_users / self.username_input
        notes_directory = directory_all / "notes"
        logs_directory = directory_all / "logs"
        private_notes_directory = notes_directory / "private"
        public_notes_directory = notes_directory / "public"

        directory_users.mkdir(parents=True, exist_ok=True)
        directory_all.mkdir(parents=True, exist_ok=True)
        notes_directory.mkdir(parents=True, exist_ok=True)
        logs_directory.mkdir(parents=True, exist_ok=True)
        private_notes_directory.mkdir(parents=True, exist_ok=True)
        public_notes_directory.mkdir(parents=True, exist_ok=True)

        # Open menu window
        from GUI.menu_interface import menu_window
        win_menu = menu_window(
            username = self.username_input,
            public_cryptography= self.public_cryptography,
            private_cryptography= self.private_cryptography,
            account_verified = self.verified_account,
            night_mode_on = self.night_mode_on
                            )
        win_menu.show()
        self.close()


    def changed_text_input(self, text, type_changed):
        """
        Checks the state of the password input every time the user types or deletes something in the box.
        
        Return a different style depending on the state of the password input box. 
        """
        
        def contains_special_characters(text):
            # Return True if there is a special character in the string, else None
            special_characters_pattern = r"[^\w\s]" # Ignores any character that is not of type \w(alphabetic characters and underscores) and \s(whitespaces)
            return bool(re.search(special_characters_pattern, text)) # searches in the string, and converts the return into a boolean


        if type_changed == "password":

            self.password_input = text


            if not text:
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))
                else: self.password_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))

                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)

            elif len(text)<8:
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif text.isupper() or text.islower():
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif not contains_special_characters(text):
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(True)

            else:
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.password_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_night))

                self.valid_password = True
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)


        elif type_changed == "priv_pass":

            self.password_input = text


            if not text:
                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))
                else: self.priv_pass_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))

                self.signin_button.setEnabled(False)
                self.valid_priv_pass = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)

            elif len(text)<8:
                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_priv_pass = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif text.isupper() or text.islower():
                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_priv_pass = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif not contains_special_characters(text):
                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_priv_pass = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(True)

            else:
                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_night))

                self.valid_priv_pass = True
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)


        elif type_changed == "username":
            
            self.username_input = text
            self.username_exists_warning.setVisible(False)

            if not text:
                if not self.night_mode_on: self.username_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_day))
                else: self.username_input_box.setStyleSheet(self.username_password_css.format(**self.username_password_night))

                self.signin_button.setEnabled(False)
                self.valid_username = False
                self.username_warning.setVisible(False)
        
            elif len(text)<5:
                if not self.night_mode_on: self.username_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.username_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

                self.signin_button.setEnabled(False)
                self.valid_username = False
                self.username_warning.setVisible(True)

            else:
                if not self.night_mode_on: self.username_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.username_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_night))

                self.valid_username = True
                self.username_warning.setVisible(False)


        pass_input = self.password_input_box.text().strip()
        priv_pass_input = self.priv_pass_input_box.text().strip()

        if pass_input == priv_pass_input and pass_input:
            self.same_password_warning.setVisible(True)

            if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
            if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

        
        else: 
            self.same_password_warning.setVisible(False)

            if self.valid_priv_pass:

                if not self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_day))
                if self.night_mode_on: self.priv_pass_input_box.setStyleSheet(self.cansign_style_css.format(**self.input_style_night))

            if self.valid_password and self.valid_username and self.valid_priv_pass:
                self.signin_button.setEnabled(True)
