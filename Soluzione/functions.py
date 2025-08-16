# -*- coding: utf-8 -*-


from pathlib import Path
import os

# Create all required folders BEFORE any other operation
directory_logs = Path(__file__).parent / "logs"
directory_logs.mkdir(exist_ok=True)

directory_all_notes = Path(__file__).parent / "notes"
directory_public_notes = directory_all_notes / "public"
directory_private_notes = directory_all_notes / "private"

directory_all_notes.mkdir(exist_ok=True)
directory_public_notes.mkdir(exist_ok=True)
directory_private_notes.mkdir(exist_ok=True)

import sqlite3
import subprocess
import logging
import getpass
from argon2 import PasswordHasher, exceptions
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

conn = sqlite3.connect(Path(__file__).parent / "credentials.db")
cursor = conn.cursor()

cursor.execute("""
    
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    publ_pass TEXT NOT NULL,
                    pub_salt BLOB,
                    priv_pass TEXT,
                    priv_salt BLOB)
                    
                """)

# Create password hasher object
pass_hash = PasswordHasher(
    time_cost=2,
    memory_cost=32 * 1024,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    """
    Returns the Argon2ID hash of the password.
    """
    return pass_hash.hash(password)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(directory_logs / "file_logs.txt"),
    filemode="a"
)

verified_account = False
notes_exists = False
repeated = True

def verify_privates(credentials_priv, attempts):
    """
    Asks the user to enter the password to access private notes.
    Allows up to 5 attempts.
    """

    
    temp_pass = password_priv  # Temporarily stores the password for encryption
    try:
        pass_hash.verify(credentials_priv, password_priv)
        logging.info("Private notes access granted")
        private_cryptography = Cryptography(temp_pass)
        logging.info("Cryptography object for private notes created successfully")
        temp_pass = None  # Removes the plain password for security
        return private_cryptography

    except Exception:
        if attempts < 4:
            logging.warning("Wrong password entered for private notes")
        else:
            logging.error("Too many failed attempts for private notes access")
            exit()

def exists_verify(username):
    """
    Checks if a password exists for private notes.
    If not, asks for and saves a new one.
    """
    
    cursor.execute("SELECT priv_pass FROM users WHERE username = ?", (username,))
    priv_pass = cursor.fetchone()[0]

        
    else:
        verify_privates(priv_pass)
        logging.info("Private notes password saved successfully")

        private_cryptography = Cryptography(temp_pass)
        logging.info("Cryptography object for private notes created successfully")
        temp_pass = None
        sleep(0.5)
        return private_cryptography

def notes_considered(del_mod):
    """
    Shows the list of notes (private and public) and asks the user which one to consider.
    Args:
        del_mod: string indicating the action (e.g. 'da eliminare', 'da aprire')
    Returns:
        (selected note index, note type: 1=private, 2=public)
    """
    sep_notes_list = [os.listdir(directory_private_notes), os.listdir(directory_public_notes)]
    notes_list_tot = sep_notes_list[0] + sep_notes_list[1]
    second_rotation = False
    print()

    for a in sep_notes_list:
        count = 1
        if not a:
            print(f"Non hai appunti {'privati' if second_rotation is False else 'pubblici'} {del_mod}")
        else:
            print("Appunti privati:") if second_rotation is False else print("Appunti pubblici:")
        for i in a:
            print(f"    {count}. {i[:-4]}")
            count += 1
            notes_list_tot.append(i)
        sleep(1.5)
        print()
        second_rotation = True

    sleep(3)

    private_cryptography = None  # Initialize variable for private encryption
    # Input request with loop until valid
    while True:
        try:
            os.system("cls")
            sleep(0.5)
            priv_publ = int(input(f"""Inserisci il numero dello stato degli appunti {del_mod}:
    1. Privati
    2. Pubblici
"""))
            if priv_publ < 1 or priv_publ > 2:
                sleep(0.5)
                print("Inserisci un numero valido")
                logging.error("Invalid number entered for note type selection")
            else:
                if priv_publ == 1:
                    if not sep_notes_list[0]: raise NotExistingNotes
                    else: private_cryptography = exists_verify()
                elif priv_publ == 2:
                    if not sep_notes_list[1]: raise NotExistingNotes
                break
        except ValueError:
            sleep(0.5)
            print()
            print("Inserisci un numero!")
            print()
            logging.error("Non-numeric value entered for note type selection")
        except NotExistingNotes:
            sleep(0.5)
            print(f"Non hai appunti {'privati' if priv_publ == 1 else 'pubblici'} {del_mod}")
            sleep(0.5)
            logging.warning(f"Attempted to select {'private' if priv_publ == 1 else 'public'} notes but none exist")
    count = 1
    os.system("cls")
    print(f"Inserisci il numero corrispondente agli appunti privati {del_mod}:") if priv_publ == 1 else print(f"Inserisci il numero corrispondente agli appunti pubblici {del_mod}:")
    for i in sep_notes_list[priv_publ-1]:
        print(f"    {count}. {i[:-4]}")
        count += 1

    notes_to_consider = None
    while True:
        try:
            notes_to_consider = int(input())
            if 1 <= notes_to_consider <= len(sep_notes_list[priv_publ-1]): break
            else:
                sleep(0.5)
                print("Numero non valido, riprova.")
                logging.error("Invalid number entered for note selection")
        except ValueError:
            sleep(0.5)
            print("Inserisci un numero.")
            logging.error("Non-numeric value entered for note selection")

    if del_mod != "da eliminare": return notes_to_consider, priv_publ, private_cryptography

    return notes_to_consider, priv_publ

def delete_notes():
    """
    Handles the procedure for deleting a note chosen by the user.
    """
    sep_notes_list = [os.listdir(directory_private_notes), os.listdir(directory_public_notes)]
    notes_to_delete, priv_publ = notes_considered("da eliminare")
    if priv_publ == 1:
        if sep_notes_list[0]:
            notes = FileNotes(directory_private_notes/sep_notes_list[0][notes_to_delete-1])
            notes.delete(sep_notes_list[0], notes_to_delete-1, directory_private_notes)
        else:
            print("Non hai appunti privati da eliminare")
            logging.warning("Attempted to delete private notes but none exist")
            return
    else:
        if sep_notes_list[1]:
            notes = FileNotes(directory_public_notes/sep_notes_list[1][notes_to_delete-1])
            notes.delete(sep_notes_list[1], notes_to_delete-1, directory_public_notes)
        else:
            print("Non hai appunti pubblici da eliminare")
            logging.warning("Attempted to delete public notes but none exist")
            return
    logging.info(f"Note deleted: {sep_notes_list[priv_publ-1][notes_to_delete-1]} in {'private' if priv_publ == 1 else 'public'}")
    sleep(0.5)


class Cryptography():
    """
    Class for file encryption and decryption.
    """
    def __init__(self, password: str, username):
        self.temp_pass = password
        self.username = username
        
        def control_salt(salt_name):
            """
            Checks if the salt exists, creates it if not, otherwise retrieves it.
            """
            
            cursor.execute("SELECT publ_salt, priv_salt FROM users WHERE username = ?", (self.username,))
            
            salts = cursor.fetchone()
            publ_salt, priv_salt = salts

            if salt_name == "publ_salt" and publ_salt is None:
                salt = secrets.token_bytes(16)
                cursor.execute("UPDATE users SET publ_salt = ? WHERE username = ?",(salt, self.username,))
                conn.commit()

            elif salt_name == "publ_salt" and publ_salt: return publ_salt

            elif salt_name == "priv_salt" and priv_salt is None:
                salt = secrets.token_bytes(16)
                cursor.execute("UPDATE users SET priv_salt = ? WHERE username = ?",(salt, self.username,))
                conn.commit()

            elif salt_name == "priv_salt" and priv_salt: return priv_salt

            return salt
        
        cursor.execute("SELECT publ_pass FROM users WHERE username = ?", self.username,)
        password = cursor.fetchone()[0]

        try:
            pass_hash.verify(password, self.temp_pass)
            self.salt = control_salt("publ_salt")

        except Exception:
            self.salt = control_salt("priv_salt")

        self.key = self.derive_key(password, self.salt)
        self.aesgcm = AESGCM(self.key)
        self.temp_pass = None  # Removes the plain password for security

    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derives an AES-GCM key from a password and a salt.
        """
        return hash_secret_raw(
            password.encode(),
            salt=salt,
            time_cost=3,
            memory_cost=64 * 1024,
            parallelism=2,
            hash_len=32,
            type=Type.ID
        )

    def encrypt(self, directory: bytes) -> bytes:
        """
        Encrypts data using AES-GCM.
        """
        with open(directory, "rb") as file:
            data = file.read()
        nonce = secrets.token_bytes(12)
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        with open(directory, "wb") as file:
            file.write(nonce + ciphertext)

    def decrypt(self, directory: bytes) -> str:
        """
        Decrypts data encrypted using AES-GCM.
        """
        with open(directory, "rb") as file:
            encrypted_data = file.read()
        nonce = encrypted_data[:12]
        cipher_text = encrypted_data[12:]
        with open(directory, "w") as file:
            decrypted_data = self.aesgcm.decrypt(nonce, cipher_text, None)
            decoded_data = decrypted_data.decode('utf-8', errors='ignore')
            file.write(decoded_data)

class Account:
    """
    Handles user account registration and verification.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_account(self):
        """
        Creates a new account and saves the credentials.
        """
        logging.info(f"Account created: {self.username}")
        credentials = {
            "username": self.username,
            "password": self.password
        }

        cursor.execute("""
        
                        INSERT INTO users(username, publ_pass) VALUES (?, ?)""", 
                        (credentials["username"], credentials["password"])
                        
                        )

        conn.commit()

        logging.info(f"Credentials saved for user: {self.username}")
        
    
    def sign_in(self):
        """
        User registration procedure.
        """
        password_temp = self.password
        self.password = hash_password(self.password)
        self.create_account()
        logging.info(f"Account registered: {self.username}")
        public_cryptography = Cryptography(password_temp, self.username)
        password_temp = None
        verified_account = True
        return verified_account, public_cryptography

    def verify_user(self):
        """
        Verifies user credentials.
        """
        
        
        cursor.execute("SELECT username, publ_pass FROM users WHERE username = ?"), (self.username,)
        credentials = cursor.fetchone()
        credentials = {
                        "username": credentials[0],
                        "password": credentials[1]
                        }

        try:
            if not credentials["username"]:
                raise VerifyError("Username non trovato")

        except VerifyError:
            logging.error("Username not found during verification")
            return False

        try:
            pass_hash.verify(credentials["password"], self.password)
            return True
        
        except exceptions.VerifyMismatchError:
            logging.error("Password doesn't match, verification failed")
            return False
        

class VerifyError(Exception):
    """
    Custom exception for account verification errors.
    """
    pass

class NotExistingNotes(Exception):
    """
    Custom exception for when notes do not exist.
    """
    pass    

class File:
    """
    Base class for file management.
    """
    def __init__(self, directory):
        self.directory = directory


class FileNotes(File):
    """
    Manages notes files (private/public).
    """
    def __init__(self, directory):
        super().__init__(directory)

    def open(self, type_cryptography):
        """
        Opens the notes file with Notepad and reports any changes.
        """
        type_cryptography.decrypt(self.directory)
        process = subprocess.Popen(["notepad.exe", self.directory])
        last_edit = os.path.getmtime(self.directory)
        while process.poll() is None:
            sleep(0.5)
            new_edit = os.path.getmtime(self.directory)
            if new_edit != last_edit:
                print("Il file è stato modificato")
                last_edit = new_edit
                logging.info(f"File {self.directory} modified")
        type_cryptography.encrypt(self.directory)

    def create(self, type_cryptography):
        """
        Creates a new notes file and opens it.
        """
        with open(self.directory, "w") as file:
            file.write("Scrivi i tuoi appunti qui")
        print("File creato correttamente!")
        logging.info(f"File created: {self.directory.name}")
        sleep(0.5)
        type_cryptography.encrypt(self.directory)
        self.open(type_cryptography)

    def delete(self, notes_list, notes_to_delete, directory_considerata):
        """
        Deletes a selected notes file.
        """
        global deleted
        for i in notes_list:
            if notes_list[notes_to_delete] == i:
                os.remove(directory_considerata / i)
                print("Appunti eliminati correttamente!")
                deleted = True
        if not deleted:
            print("Numero non valido")

