# -*- coding: utf-8 -*-

from pathlib import Path
import importlib.util

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)


from PySide6.QtWidgets import QApplication, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt, QSize
from PySide6.QtGui import QIcon, QGuiApplication

images_path = Path(__file__).parent / "Images"

class verify_identity_window(QWidget):

    def __init__(self, username, public_cryptography, private_cryptography, night_mode_on):
        super().__init__()

        # Variables initialization

        self.username = username
        self.public_cryptography = public_cryptography
        self.private_cryptography = private_cryptography
        self.night_mode_on = night_mode_on

        self.valid_username = False
        self.valid_password = False
        self.hidden_password = True
        self.user_verified = False

        # Window initialization
        self.setWindowTitle("Verifica account")
        self.setFixedSize(500, 650)

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)


        # Input camps and texts initialization

        self.username_input_box = QLineEdit()
        
        self.password_input_box = QLineEdit()

        self.password_hide_button = QPushButton("")

        self.login_button = QPushButton("Verifica")

        self.login_text = QLabel("Verifica il tuo account")

        self.warning_text = QLabel("Password per file privati non valida o non trovata")

        self.warning_attempts = QLabel("Troppi tentativi falliti, riprova pi\u00f9 tardi")

        self.goback_menu = QPushButton("Torna al men\u00f9 principale")

        
        # Commons styles

        self.button_style = """
        
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

        self.username_password_css = """
            
                                        background-color: {background_color}; 
                                        font-size: 16px;
                                        font-family: Arial;
                                        border: 1px solid {border_color};
                                        border-radius: 12px;
                                        color: {text_color};
                                        padding-left: 3px;
            
                                    """

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
                                    font-size: 15px;
                                    color: red;
                                
                                """

        self.tools_style = """
            
            QPushButton
            {{
                border-radius: 15px;
                background-color: {normal_background_color};
                border: 1px solid {normal_border_color};
                color: {normal_text_color};
            }}

            QPushButton:hover
            {{
                border-radius: 15px;
                background-color: {hover_background_color};
                border: 1px solid {hover_border_color};
                color: {hover_text_color};
            }}

            QPushButton:pressed
            {{
                border-radius: 15px;
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


        # Input camps and text modellation
        
        self.password_input_box.setPlaceholderText("Password per i file privati")
        self.password_input_box.setFixedSize(350, 40)
        self.password_input_box.setEchoMode(QLineEdit.Password) # Hides the password input by default
        self.password_input_box.textChanged.connect(self.changed_text_input)
        
        self.login_text.setAlignment(Qt.AlignCenter)

        self.login_button.setFixedSize(350, 45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setEnabled(False)
        self.login_button.setStyleSheet(self.button_style)
        self.attempts = 0
        self.login_button.clicked.connect(self.verify_clicked_func)

        self.password_hide_button.setFixedSize(40, 25)
        self.password_hide_button.setIconSize(QSize(30, 30))
        self.password_hide_button.setCursor(Qt.PointingHandCursor)
        self.password_hide_button.setStyleSheet("""
        
            background-color: transparent;
            border: none;

                                                """)
        self.password_hide_button.clicked.connect(self.hide_password_func)

        self.warning_text.setVisible(False)
        self.warning_text.setAlignment(Qt.AlignCenter)
        self.warning_text.setStyleSheet(self.warning_text_css)
        
        self.warning_attempts.setVisible(False)
        self.warning_attempts.setAlignment(Qt.AlignCenter)
        self.warning_attempts.setStyleSheet(self.warning_text_css)

        self.goback_menu.setFixedSize(300, 30)
        self.goback_menu.setCursor(Qt.PointingHandCursor)
        self.goback_menu.clicked.connect(self.exit)

        
        if not self.night_mode_on:

            self.setStyleSheet("background-color: #f2f2f2")

            self.password_input_box.setStyleSheet(self.username_password_css.format(
                
                                                       background_color = "white",
                                                       text_color = "black",
                                                       border_color = "#ccc"
            
                                                                                    ))

            self.login_text.setStyleSheet("""
            
            font-family: 'Merriweather', serif;
            font-weight: 500;
            font-style: italic;
            font-size: 25px;
            color: black;
            margin-bottom: 50px;
        
                                    """)

            self.dir_close_eye = images_path / "eye_close_day.png"
            self.dir_open_eye = images_path / "eye_open_day.png"

            self.password_hide_button.setIcon(QIcon(str(self.dir_close_eye)))

            self.goback_menu.setStyleSheet(self.tools_style.format(**self.tools_style_day))


        else:

            self.setStyleSheet("background-color: #1C1C1E")

            self.password_input_box.setStyleSheet(self.username_password_css.format(
            
                                                      background_color = "#3A3A3C",
                                                      border_color = "#5A5A5C",
                                                      text_color = "white",
            
                                                                                    ))

            self.login_text.setStyleSheet("""
            
            font-family: 'Merriweather', serif;
            font-weight: 500;
            font-style: italic;
            font-size: 25px;
            color: white;
            margin-bottom: 50px;
        
                                    """)

            self.dir_close_eye = images_path / "eye_close_night.png"
            self.dir_open_eye = images_path / "eye_open_night.png"

            self.password_hide_button.setIcon(QIcon(str(self.dir_close_eye)))

            self.goback_menu.setStyleSheet(self.tools_style.format(**self.tools_style_night))


        # Layout Initialization
        layout = QVBoxLayout()

        # Button's layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        # Hide password button functionality
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input_box)
        password_layout.addWidget(self.password_hide_button)

        # goback menu layout

        self.goback_interface = QHBoxLayout()
        self.goback_interface.addWidget(self.goback_menu)
        self.goback_interface.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        # layout configuration
        layout.addWidget(self.login_text)
        layout.addLayout(password_layout)
        layout.addWidget(self.warning_text)
        layout.addWidget(self.warning_attempts)
        layout.addWidget(self.login_button)
        layout.addLayout(self.goback_interface)
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout) 
        
        layout.setContentsMargins(75, 0, 75, 100)
        self.setLayout(layout)


    # Connect the buttons to the functions


    def hide_password_func(self):
        """
        Function to hide or show the password in the password input box when the user clicks on the eye button.
        """
        self.hidden_password = not self.hidden_password  # Toggle the hidden password state

        if self.hidden_password: self.password_hide_button.setIcon(QIcon(str(self.dir_close_eye))); self.password_input_box.setEchoMode(QLineEdit.Password)
        else: self.password_hide_button.setIcon(QIcon(str(self.dir_open_eye))); self.password_input_box.setEchoMode(QLineEdit.Normal)


    def verify_clicked_func(self):
        """
        Function to call after the user clicks on the signin button.
        """

        # Reads the inputs from the input boxes and tries to sign in
        self.password_input = self.password_input_box.text().strip()
        self.attempts += 1

        self.password_input_box.clear()

        
        if self.attempts <= 3:

            account = functions.Account(username = self.username, priv_pass = self.password_input)
            self.verified_account, self.private_cryptography = account.verify_priv_user()

            # self.verified_account = functions.verify_privates()
            if self.verified_account:
                from GUI.menu_interface import menu_window
                menu_win = menu_window(
                    username = self.username,
                    public_cryptography = self.public_cryptography,
                    private_cryptography = self.private_cryptography,
                    account_verified = self.verified_account,
                    night_mode_on = self.night_mode_on
                                    )
                menu_win.show()
                self.close()

            else: 
                self.warning_text.setVisible(True); 
                if not self.night_mode_on: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_day))
                else: self.password_input_box.setStyleSheet(self.warning_style_css.format(**self.input_style_night))

        else:
            self.warning_text.setVisible(False)
            self.warning_attempts.setVisible(True)
            self.login_button.setEnabled(False)


    def changed_text_input(self):
        """
        Function that checks if the username and password input boxes are filled
        """
        
        input_password = self.password_input_box.text().strip()

        if self.attempts <= 3:
            if input_password: self.login_button.setEnabled(True) 
            else: self.login_button.setEnabled(False)


    def exit(self):
        """
        Function tu return to the main menu if the user clicks on the goback button.
        """
        
        from GUI.menu_interface import menu_window
        win_menu = menu_window(
            username=self.username,
            public_cryptography=self.public_cryptography,
            private_cryptography=self.private_cryptography,
            account_verified=self.user_verified,
            night_mode_on=self.night_mode_on
        )

        win_menu.show()
        self.close()