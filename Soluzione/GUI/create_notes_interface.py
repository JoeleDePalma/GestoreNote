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
    def __init__(self, username):
        super().__init__()
        self.username = username

        # Window initialization
        self.setWindowTitle("Crea note")
        self.setFixedSize(400, 200)

        # Input camps and texts initialization
        self.note_title_input_box = QLineEdit()
        self.save_public_button = QPushButton("Salva nota pubblica")
        self.save_private_button = QPushButton("Salva nota privata")

        # Commons styles

        self.buttons_style = """
        
            QPushButton 
            {
                background-color: #007BFF;  
                color: white;  
                border: 1px solid black;  
                border-radius: 10px; 
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
        

        # Input camps and texts modellation
        self.note_title_input_box.setPlaceholderText("Titolo della nota")
        self.note_title_input_box.setFixedSize(350, 60)
        self.note_title_input_box.setStyleSheet("""
        
                                        background-color: white; 
                                        font-size: 16px;
                                        font-family: Arial;
                                        border: 1px solid #ccc;
                                        border-radius: 20px;
                                        margin-bottom: 20px;
        
                            
                                                """)

        self.save_private_button.setFixedSize(175, 40)
        self.save_private_button.setStyleSheet(self.buttons_style)
        self.save_private_button.clicked.connect(lambda: self.create_notes(f"{self.note_title_input_box.text().strip()}.txt", public=False))

        self.save_public_button.setFixedSize(175, 40)
        self.save_public_button.setStyleSheet(self.buttons_style)
        self.save_public_button.clicked.connect(lambda: self.create_notes(f"{self.note_title_input_box.text().strip()}.txt", public=True))


        # buttons layout
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.save_public_button)
        self.buttons_layout.addWidget(self.save_private_button)
        self.buttons_layout.setAlignment(Qt.AlignCenter)

        # Layouts initialization
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.note_title_input_box)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.buttons_layout)


    def create_notes(self, notes_name, public):
        if public:
            file = functions.FileNotes(Path(__file__).parent.parent / self.username / "notes" / "public" / notes_name)
            created = file.create()

        else: 
            file = functions.FileNotes(Path(__file__).parent.parent / self.username / "notes" / "private" / notes_name)
            created = file.create()

        if created:
            from GUI.menu_interface import menu_window
            win_menu = menu_window(self.username)
            win_menu.show()
            self.close()

        else:
            error_label = QLabel("Errore durante la creazione della nota.")
            error_label.setStyleSheet("color: red; font-size: 16px;")
            self.layout.addWidget(error_label)
            self.layout.setAlignment(Qt.AlignCenter)
