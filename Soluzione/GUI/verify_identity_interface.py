# -*- coding: utf-8 -*-

from pathlib import Path
import importlib.util

# functions_path = Path(__file__).parent.parent / "functions.py"

# spec = importlib.util.spec_from_file_location("functions", str(functions_path))
# functions = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(functions)


from PySide6.QtWidgets import QApplication, QLineEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt, QSize
from PySide6.QtGui import QIcon

images_path = Path(__file__).parent / "Images"

class verify_identity__window(QWidget):

    def __init__(self):
        super().__init__()

        # Variables initialization

        self.valid_username = False
        self.valid_password = False
        self.hidden_password = True
        self.user_verified = False

        # Window initialization
        self.setWindowTitle("Verifica account")
        self.setFixedSize(500, 650)


        # Input camps and texts initialization

        self.username_input_box = QLineEdit()
        
        self.password_input_box = QLineEdit()

        self.password_hide_button = QPushButton(QIcon(str(images_path / "eye_close.png")), "")

        self.login_button = QPushButton("Verifica")

        self.login_text = QLabel("Verifica il tuo account")

        self.warning_text = QLabel("Nome utente o password non validi")

        self.warning_attempts = QLabel("Troppi tentativi falliti, riprova pi\u00f9 tardi")


        
        # Commons styles
        self.username_password_css = """
            
                                        background-color: white; 
                                        font-size: 16px;
                                        font-family: Arial;
                                        border: 1px solid #ccc;
                                        border-radius: 12px;
            
                                    """

        self.warning_style_css = """
            
                                    background-color: white; 
                                    font-size: 16px;
                                    font-family: Arial;
                                    border: 1px solid red;
                                    border-radius: 12px;
            
                                """

        self.cansign_style_css = """
                
                                    background-color: white; 
                                    font-size: 16px;
                                    font-family: Arial;
                                    border: 1px solid green;
                                    border-radius: 12px;

                                """

        self.warning_text_css = """
                                
                                    font-family: Arial;
                                    font-size: 15px;
                                    color: red;
                                
                                """

        # Input camps and text modellation
        
        self.password_input_box.setPlaceholderText("Password")
        self.password_input_box.setFixedSize(350, 40)
        self.password_input_box.setStyleSheet(self.username_password_css)
        self.password_input_box.setEchoMode(QLineEdit.Password) # Hides the password input by default
        self.password_input_box.textChanged.connect(self.changed_text_input)
        
        self.login_text.setAlignment(Qt.AlignCenter)
        self.login_text.setStyleSheet("""
            
            font-family: 'Merriweather', serif;
            font-weight: 500;
            font-style: italic;
            font-size: 25px;
            color: black;
            margin-bottom: 50px;
        
        """)

        self.login_button.setFixedSize(350, 45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setEnabled(False)
        self.login_button.setStyleSheet("""
        
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
        self.attempts = 0
        self.login_button.clicked.connect(self.verify_clicked_func)

        self.password_hide_button.setFixedSize(50, 30)
        self.password_hide_button.setIconSize(QSize(40, 40))
        self.password_hide_button.setStyleSheet("""
        
                                                    background-color: transparent;
                                                    border: none;

                                                """)
        self.password_hide_button.setCursor(Qt.PointingHandCursor)
        self.password_hide_button.clicked.connect(self.hide_password_func)

        self.warning_text.setVisible(False)
        self.warning_text.setAlignment(Qt.AlignCenter)
        self.warning_text.setStyleSheet(self.warning_text_css)
        
        self.warning_attempts.setVisible(False)
        self.warning_attempts.setAlignment(Qt.AlignCenter)
        self.warning_attempts.setStyleSheet(self.warning_text_css)


        # Layout Initialization
        layout = QVBoxLayout()

        # Button's layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        # Hide password button functionality
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input_box)
        password_layout.addWidget(self.password_hide_button)
        
        # layout configuration
        layout.addWidget(self.login_text)
        layout.addLayout(password_layout)
        layout.addWidget(self.warning_text)
        layout.addWidget(self.warning_attempts)
        layout.addWidget(self.login_button)
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

        if self.hidden_password: self.password_hide_button.setIcon(QIcon(str(images_path / "eye_close.png"))); self.password_input_box.setEchoMode(QLineEdit.Password)
        else: self.password_hide_button.setIcon(QIcon(str(images_path / "eye_open.png"))); self.password_input_box.setEchoMode(QLineEdit.Normal)


    def verify_clicked_func(self):
        """
        Function to call after the user clicks on the signin button.
        """

        # Reads the inputs from the input boxes and tries to sign in
        self.password_input = self.password_input_box.text().strip()
        self.attempts += 1

        self.password_input_box.clear()

        if self.attempts < 3:
            # self.verified_account = functions.verify_privates()
            if self.verified_account is True:
                from GUI.menu_interface import menu_window
                menu_win = menu_window()
                menu_win.show()
                self.close()

            else: self.warning_text.setVisible(True)

        else:
            self.warning_text.setVisible(False)
            self.warning_attempts.setVisible(True)
            self.login_button.setEnabled(False)


    def changed_text_input(self):
        """
        Function that checks if the username and password input boxes are filled
        """
        
        input_password = self.password_input_box.text().strip()

        if self.attempts < 3:
            if input_password: self.login_button.setEnabled(True) 
            else: self.login_button.setEnabled(False)
        


app = QApplication([])
window = verify_identity__window()
window.show()
app.exec()