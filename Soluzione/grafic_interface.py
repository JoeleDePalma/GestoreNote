# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QApplication, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt
from functions import *
import re

class login_window(QWidget):

    def __init__(self):
        super().__init__()

        # Variables initialization

        self.valid_username = False
        self.valid_password = False

        # Window initialization
        self.setWindowTitle("Registrati")
        self.setFixedSize(500, 650)


        # Input camps and texts initialization
        self.welcome_text = QLabel("Benvenuto!")

        self.username_input_box = QLineEdit()

        self.username_warning = QLabel("Il nome utente deve essere lungo almeno 5 caratteri")
        
        self.password_input_box = QLineEdit()

        self.password_warning = QLabel("La password deve contenere almeno 8 caratteri maiuscoli e minuscoli")

        self.characters_warning = QLabel("La password deve contere almeno un carattere speciale")

        self.signin_button = QPushButton("Registrati")

        self.signin_text = QLabel("Crea il tuo account")

        self.login_link = QPushButton("Accedi")

        
        
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
                                    font-size: 10px;
                                    color: red;
                                
                                """

        # Input camps and text modellation
        self.welcome_text.setAlignment(Qt.AlignCenter)
        self.welcome_text.setStyleSheet("""
            
            font-family: Montserrat;
            font-size: 30px;
            font-weight: bold;
        
        """)
        
        self.username_input_box.setPlaceholderText("Nome utente")
        self.username_input_box.setFixedSize(350, 40)
        self.username_input_box.setStyleSheet(self.username_password_css)
        self.username_input_box.textChanged.connect(lambda text: self.changed_text_input(text, "username"))

        self.password_input_box.setPlaceholderText("Password")
        self.password_input_box.setFixedSize(350, 40)
        self.password_input_box.setStyleSheet(self.username_password_css)
        self.password_input_box.textChanged.connect(lambda text: self.changed_text_input(text, "password"))

        self.login_link.setFlat(True)
        self.login_link.setFixedSize(60, 20)
        self.login_link.setCursor(Qt.PointingHandCursor)
        self.login_link.setStyleSheet("""
            
            QPushButton 
            {
                font-family: Poppins semibold;
                font-size: 15px;
                background: transparent !important;  /* Forza lo sfondo trasparente */
                text-decoration: underline;
                color: #007BFF;  /* Colore normale */
                border: none !important;  /* Rimuove qualsiasi bordo */
                padding: 0 !important;  /* Rimuove il padding */
            }

            QPushButton:hover 
            {
                color: #0056b3;  /* Colore quando il cursore è sopra */
                background: transparent !important;  /* Forza lo sfondo trasparente */
            }

            QPushButton:pressed 
            {
                color: #004085;  /* Colore quando il pulsante è cliccato */
                background: transparent !important;  /* Forza lo sfondo trasparente */
            }

        """)

        self.signin_text.setAlignment(Qt.AlignCenter)
        self.signin_text.setStyleSheet("""
            
            font-family: Arial;
            font-size: 15px;
            color: grey;
            margin-bottom: 50px;
        
        """)

        self.signin_button.setFixedSize(350, 45)
        self.signin_button.setCursor(Qt.PointingHandCursor)
        self.signin_button.setEnabled(False)
        self.signin_button.setStyleSheet("""
        
            QPushButton 
            {
                background-color: #007BFF;  /* Colore di sfondo */
                color: white;  /* Colore del testo */
                border: none;  /* Rimuove il bordo */
                border-radius: 20px;  /* Angoli arrotondati */
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


        # Layout Initialization
        layout = QVBoxLayout()

        # Button's layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_link)
        button_layout.setAlignment(Qt.AlignCenter)

        # layout configuration
        layout.addWidget(self.welcome_text)
        layout.addWidget(self.signin_text)
        layout.addWidget(self.username_input_box)
        layout.addWidget(self.username_warning)
        layout.addWidget(self.password_input_box)
        layout.addWidget(self.password_warning)
        layout.addWidget(self.characters_warning)
        layout.addWidget(self.signin_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout) 
        
        layout.setContentsMargins(0, 0, 0, 100)
        self.setLayout(layout)


    # Connect the buttons to the functions
    def signin_clicked_func(self):
        """
        Function to call after the user clicks on the signin button.
        """

        # Reads the inputs from the input boxes and tries to sign in
        self.username_input = self.username_input_box.text()
        self.password_input = self.password_input_box.text()
        account = Account(username=self.username_input, password=self.password_input)
        self.verified_account, self.public_cryptography = account.sign_in()

        # If the account is verified, we can proceed to the main window
        self.password_input_box.clear()
        self.username_input_box.clear()
        

    def changed_text_input(self, text, type_changed):
        """
        Checks the state of the password input every time the user types or deletes something in the box.
        
        Return a different style depending on the state of the password input box. 
        """
        
        if type_changed == "password":

            self.password_input = text

        
            def contains_special_characters(text):
                # Return True if there is a special character in the string, else None
                special_characters_pattern = r"[^\w\s]" # Ignores any character that is not of type \w(alphabetic characters and underscores) and \s(whitespaces)
                return bool(re.search(special_characters_pattern, text)) # searches in the string, and converts the return into a boolean


            if not text:
                self.password_input_box.setStyleSheet(self.username_password_css)
                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)

            elif len(text)<8:
                self.password_input_box.setStyleSheet(self.warning_style_css)
                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif text.isupper() or text.islower():
                self.password_input_box.setStyleSheet(self.warning_style_css)
                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(True)
                self.characters_warning.setVisible(False)

            elif not contains_special_characters(text):
                self.password_input_box.setStyleSheet(self.warning_style_css)
                self.signin_button.setEnabled(False)
                self.valid_password = False
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(True)

            else:
                self.password_input_box.setStyleSheet(self.cansign_style_css)
                self.valid_password = True
                self.password_warning.setVisible(False)
                self.characters_warning.setVisible(False)

        elif type_changed == "username":
            
            self.username_input = text

            if not text:
                self.username_input_box.setStyleSheet(self.username_password_css)
                self.signin_button.setEnabled(False)
                self.valid_username = False
                self.username_warning.setVisible(False)
        
            elif len(text)<5:
                self.username_input_box.setStyleSheet(self.warning_style_css)
                self.signin_button.setEnabled(False)
                self.valid_username = False
                self.username_warning.setVisible(True)

            else:
                self.username_input_box.setStyleSheet(self.cansign_style_css)
                self.valid_username = True
                self.username_warning.setVisible(False)

        if self.valid_password and self.valid_username:
            self.signin_button.setEnabled(True)


def delete_item(self, item_to_delete) -> bool:

    for i in range(self.layout.count()):

        item = self.layout.itemAt(i)

        if item.widget() and item.widget() == item_to_delete:
            self.layout.takeAt(i)  # Deletes the item from the layout
            item_to_delete.deleteLater()  # Deletes the widget from the memory
            return True  # Indicates that the item was found and deleted

    return False  # Indicates that the item was not found

app = QApplication([])
window = login_window()
window.show()
app.exec()