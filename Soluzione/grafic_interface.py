from PySide6.QtWidgets import QApplication, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QLine, Qt
from functions import *

class login_window(QWidget):

    def __init__(self):
        super().__init__()

        # Window initialization
        self.setWindowTitle("Registrati")
        self.setFixedSize(500, 650)


        # Input camps and texts initialization
        self.welcome_text = QLabel("Benvenuto!")

        self.user_input = QLineEdit()
        
        self.password_input = QLineEdit()

        self.signin_button = QPushButton("Registrati")

        self.signin_text = QLabel("Crea il tuo account")

        self.login_link = QPushButton("Accedi")

        
        
        # Commons styles
        username_password_css = """
            
            background-color: white; 
            font-size: 16px;
            font-family: Arial;
            border: 1px solid #ccc;
            border-radius: 12px;
            
        """


        # Input camps and text modellation
        self.welcome_text.setAlignment(Qt.AlignCenter)
        self.welcome_text.setStyleSheet("""
            
            font-family: Montserrat;
            font-size: 30px;
            font-weight: bold;
        
        """)

        self.user_input.setPlaceholderText("Nome utente")
        self.user_input.setFixedSize(350, 40)
        self.user_input.setStyleSheet(username_password_css)

        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(350, 40)
        self.password_input.setStyleSheet(username_password_css)


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

        self.signin_button.setFixedSize(350, 40)
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


        # Layout Initialization
        layout = QVBoxLayout()

        # Button's layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_link)
        button_layout.setAlignment(Qt.AlignCenter)

        # layout configuration
        layout.addWidget(self.welcome_text)
        layout.addWidget(self.signin_text)
        layout.addWidget(self.user_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.signin_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(button_layout) 
        
        layout.setContentsMargins(0, 0, 0, 100)
        self.setLayout(layout)


app = QApplication([])
window = login_window()
window.show()
app.exec()
