# -*- coding: utf-8 -*-


from pathlib import Path
import importlib.util

functions_path = Path(__file__).parent.parent / "functions.py"

spec = importlib.util.spec_from_file_location("functions", str(functions_path))
functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(functions)

from PySide6.QtWidgets import QApplication, QToolBar, QLineEdit, QTextEdit, QSpacerItem, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint
from PySide6.QtGui import QIcon, QGuiApplication
import sqlite3
import os

conn = sqlite3.connect(Path(__file__).parent.parent / "credentials.db")
cursor = conn.cursor()

images_path = Path(__file__).parent / "images"

class menu_window(QWidget):
    
    def __init__(self, username, public_cryptography, private_cryptography, night_mode_on, account_verified = False):
        super().__init__()
        self.username = username
        self.public_cryptography = public_cryptography
        self.private_cryptography = private_cryptography
        self.account_verified = account_verified
        self.night_mode_on = night_mode_on

        self.note = None
        self.notes_opened = None
        self.notes_opened_state = None

        self.setWindowTitle("Menu")
        self.setFixedSize(1000, 600)
        self.setStyleSheet("background-color: #f2f2f2;")

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        self.move(x, y)
        
        # Initialization variables

        self.toolbar_list = []
        self.tools_notes_list = []
        self.tools_settings_list = []

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

        self.notes_box_style = """
            
            QTextEdit{{
            
                    color: {text_color};
                    background-color: {background_color};
                    border: 1px solid {border_color};
                    font-size: 16px;
                    border-radius: 10px;
                    
            }}
                               """


        self.buttons_style_day = dict(
                     
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

        self.buttons_style_night = dict(
                     
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

        self.notes_box_style_day = dict(
            
                text_color = "black",
                background_color = "white",
                border_color="black"
                                      
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


        if self.account_verified:
            self.toolbar_settings_verify = QPushButton(QIcon(str(images_path / "verified_icon.png")), " Verificato")

        else: 
            self.toolbar_settings_verify = QPushButton(QIcon(str(images_path / "not_verified_icon.png")), " Verifica")

        self.tools_settings_list.append(self.toolbar_settings_verify)


        self.toolbar_settings_exit = QPushButton(QIcon(str(images_path / "exit_icon.jpg")), "Esci")
        self.tools_settings_list.append(self.toolbar_settings_exit)

        self.toolbar_settings_advanced = QPushButton("Avanzate")
        self.tools_settings_list.append(self.toolbar_settings_advanced)

        self.notes_text_box = QTextEdit()


        # Input camps and text modellation

        self.toolbar_nightmode_button.clicked.connect(lambda: self.night_mode(to_change = True))

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

        self.toolbar_notes_save.clicked.connect(self.save_note)

        self.toolbar_settings_exit.clicked.connect(self.exit)

        self.toolbar_notes_rename.clicked.connect(self.rename_notes_func)

        self.toolbar_notes_delete.clicked.connect(self.delete_note)

        self.toolbar_settings_verify.clicked.connect(lambda: self.verify_identity)

        self.notes_text_box.setFixedSize(550, 550)
        self.notes_text_box.setStyleSheet(self.notes_box_style.format(**self.notes_box_style_day))

        self.toolbar_settings_verify.clicked.connect(self.verify_identity)

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
        self.notes_directory = Path(__file__).parent.parent / "users" / self.username / "notes"
        self.notes_buttons = [[], []]

        self.notes_layout = QVBoxLayout()

        self.set_notes(style = self.buttons_style_day)

        self.notes_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Notes text box layout configuration

        self.notes_text_box_layout = QVBoxLayout()
        self.notes_text_box_layout.addWidget(self.notes_text_box)
        self.notes_text_box_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # main layout configuration

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.toolbar_layout)
        self.main_layout.addLayout(self.notes_text_box_layout)
        self.main_layout.addLayout(self.notes_layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        # layout configuration

        self.layout.addWidget(self.profile_button)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)

        # checks if night mode is on and sets the right styles
        self.night_mode(to_change = False)


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
        """
        Adds or modify the notes layout with notes buttons
        """

        # Verify the existence of the notes directoriess, if not, creates them
        public_dir = self.notes_directory / "public"
        private_dir = self.notes_directory / "private"

        if not public_dir.exists():
            print(f"Directory pubblica non trovata: {public_dir}")
            self.notes_text_box.setPlaceholderText("La directory degli appunti pubblici non esiste.")
            os.mkdir(public_dir)
            return

        if not private_dir.exists():
            print(f"Directory privata non trovata: {private_dir}")
            self.notes_text_box.setPlaceholderText("La directory degli appunti privati non esiste.")
            os.mkdir(private_dir)
            return

        self.public_notes = os.listdir(self.notes_directory/"public")
        self.private_notes = os.listdir(self.notes_directory/"private")
        self.sep_notes_list = [self.public_notes, self.private_notes]

        while self.notes_layout.count():
            item = self.notes_layout.takeAt(0)  
            widget = item.widget()
            if widget is not None:
                widget.deleteLater() 

        self.notes_buttons[0].clear()
        self.notes_buttons[1].clear()

        def visibility(buttons_list, public = True):

            def show_hide():
                nonlocal buttons_list
                is_visible = buttons_list[0].isVisible() if buttons_list else False
                for button in buttons_list:
                    button.setVisible(not is_visible)
            
            if public: show_hide()

            else:
                if self.account_verified: show_hide()
                
                else: 
                    self.notes_text_box.clear(); 
                    self.notes_text_box.setPlaceholderText(
'''Account non verificato. Impossibile aprire le note private.
Per verificare la tua identità, vai nelle impostazioni e clicca su "Verifica"''')
                    self.note = None
                    self.notes_opened = None
                    self.notes_opened_state = None
            

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
                        button.clicked.connect(lambda checked, note_name = j, state="public": self.open_note_func(note_name, state))
                        self.notes_buttons[0].append(button)
                        self.notes_layout.addWidget(button)

            if i == 1:
                style["margin"] = "-15px"
                self.private_notes_button = QPushButton("Appunti privati")
                self.private_notes_button.setFixedSize(160, 30)
                self.private_notes_button.setVisible(visible)
                self.private_notes_button.setStyleSheet(self.notes_style.format(**style))
                self.private_notes_button.clicked.connect(lambda: visibility(self.notes_buttons[1], False))
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
                        button.clicked.connect(lambda checked, note_name = j, state="private": self.open_note_func(note_name, state))
                        self.notes_buttons[1].append(button)
                        self.notes_layout.addWidget(button)


    def notes_appear(self, hide = False):
        """
        Shows or hides the notes buttons and the public/private notes buttons.
        """
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
        win_create = create_notes_window(
            username = self.username, 
            private_cryptography = self.private_cryptography, 
            public_cryptography = self.public_cryptography, 
            account_verified = self.account_verified,
            night_mode_on=self.night_mode_on
            )
        win_create.show()
        self.close() 

    
    def rename_notes_func(self):
        """
        Opens the rename notes interface if a note is opened.
        """
        if self.note:
            try:
                from GUI.rename_notes_interface import rename_notes_window
                # Salva l'istanza della finestra di rinomina come attributo della classe
                self.rename_win = rename_notes_window(
                    username=self.username,
                    private_cryptography=self.private_cryptography,
                    public_cryptography=self.public_cryptography,
                    account_verified=self.account_verified,
                    title=self.notes_opened,
                    state=self.notes_opened_state,
                    night_mode_on=self.night_mode_on
                )
                self.rename_win.show()
                self.close()  # Chiudi la finestra principale solo dopo aver aperto la finestra di rinomina
            except Exception as e:
                self.notes_text_box.setPlaceholderText(f"Errore durante l'apertura della finestra di rinomina: {str(e)}")
        else:
            self.notes_text_box.setPlaceholderText("Nessuna nota aperta per la rinomina.")


    def night_mode(self, to_change):

        if to_change: self.night_mode_on = not self.night_mode_on
        
        if self.night_mode_on:

            style_notes = dict(
                
                text_color= "white", 
                background_color = "#3A3A3C",
                border_color="#5A5A5C"
                
                )

            self.toolbar_nightmode_button.setText("🌞 Modalità giorno")

            self.set_tools(120, style = self.buttons_style_night)

            self.buttons_style_night["margin"] = "-15px"
            self.public_notes_button.setStyleSheet(self.notes_style.format(**self.buttons_style_night))
            self.private_notes_button.setStyleSheet(self.notes_style.format(**self.buttons_style_night))
            
            self.buttons_style_night["margin"] = "0px"
            for i in range(2):
                for j in self.notes_buttons[i]:
                    j.setStyleSheet(self.notes_style.format(**self.buttons_style_night))
            self.notes_appear(hide = True)

            self.buttons_style_night.pop("margin")

            self.toolbar_notes_show.setText("Mostra")

            self.profile_button.setStyleSheet(self.tools_style.format(**self.buttons_style_night))
            
            self.setStyleSheet("background-color: #1C1C1E")

            self.notes_text_box.setStyleSheet(self.notes_box_style.format(**style_notes))
            

        else:

            style_notes = dict(
                
                text_color= "black", 
                background_color = "white",
                border_color= "black"
                
                )

            self.toolbar_nightmode_button.setText("🌙 Modalità notte")

            self.set_tools(120, style = self.buttons_style_day)

            self.buttons_style_day["margin"] = "-15px"
            self.public_notes_button.setStyleSheet(self.notes_style.format(**self.buttons_style_day))
            self.private_notes_button.setStyleSheet(self.notes_style.format(**self.buttons_style_day))
            
            self.buttons_style_night["margin"] = "0px"
            for i in range(2):
                for j in self.notes_buttons[i]:
                    j.setStyleSheet(self.notes_style.format(**self.buttons_style_day))
            self.notes_appear(hide = True)
            
            self.buttons_style_night.pop("margin")

            self.toolbar_notes_show.setText("Mostra")

            self.profile_button.setStyleSheet(self.tools_style.format(**self.buttons_style_day))   
            
            self.setStyleSheet("background-color: #f2f2f2")

            self.notes_text_box.setStyleSheet(self.notes_box_style.format(**style_notes))
    

    def open_note_func(self, note_name, state):
        """
        Shows in the notes text box the content of the note selected.
        """

        self.note = functions.FileNotes(Path(__file__).parent.parent / "users" / self.username / "notes" / state / note_name)
        self.notes_opened = note_name
        self.notes_opened_state = state

        if state == "public": 
            text = self.note.open_note(self.public_cryptography)

        elif state == "private":
            if self.account_verified:
                text = self.note.open_note(self.private_cryptography)

            else:
                self.notes_text_box.clear()
                self.notes_text_box.setPlaceholderText("Account non verificato. Impossibile aprire la nota.")
                self.note = None
                return

        if text:
            self.notes_text_box.setPlainText(text)

        else:
            self.notes_text_box.clear()
            self.notes_text_box.setPlaceholderText("Scrivi i tuoi appunti qui")
        
    
    def save_note(self):
        """
        Save the content of the notes text box into the opened note.
        """
        text = self.notes_text_box.toPlainText()
        if self.note:
            self.note.save(text, self.public_cryptography)
            
            if not text: self.notes_text_box.setPlaceholderText("Appunti salvati con successo.")

        else:
            self.notes_text_box.setPlaceholderText("Nessuna nota aperta per il salvataggio.")


    def delete_note(self):
        if self.note:
            if self.note.delete():
                self.notes_text_box.clear()
                self.notes_text_box.setPlaceholderText("Nota eliminata con successo.")
                self.note = None
                self.set_notes(self.buttons_style_day if not self.night_mode_on else self.buttons_style_night, visible = True)
            
            else: self.notes_text_box.setPlaceholderText("Errore durante l'eliminazione della nota.")

        else: self.notes_text_box.setPlaceholderText("Nessuna nota aperta per l'eliminazione.")


    def exit(self):
        """
        Go back to the sign-in interface.
        """
        from GUI.signin_interface import signin_window
        win_signin = signin_window(self.night_mode_on)
        win_signin.show()
        self.close()


    def tools_settings_show(self):
        """
        Shows/hides the tools for settings management.
        """
        is_visible = self.tools_settings_list[0].isVisible()
        for i in self.tools_settings_list:
            i.setVisible(not is_visible)


    def tools_notes_show(self):
        """
        Shows/hides the tools for notes management.
        """
        is_visible = self.toolbar_notes_show.isVisible()
        for i in self.tools_notes_list:
            i.setVisible(not is_visible)


    def close_app(self):
        """
        Close the application and the database connection.
        """
        self.close()
        cursor.close()
        conn.close()

        
    def verify_identity(self):
        """
        Opens the verify identity interface.
        """

        if not self.account_verified:
            from GUI.verify_identity_interface import verify_identity_window
            self.win_verify = verify_identity_window(
                username=self.username,
                private_cryptography=self.private_cryptography, 
                public_cryptography = self.public_cryptography,
                night_mode_on = self.night_mode_on
                )
            self.win_verify.show()
            self.close()
            
        else:
            self.notes_text_box.setPlaceholderText(
                "Account già verificato. Non è possibile verificare nuovamente l'identità.")
