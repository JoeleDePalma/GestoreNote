# -*- coding: utf-8 -*-


from pathlib import Path
import os
import sqlite3
import logging
from argon2 import PasswordHasher, exceptions
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

dir_db = Path(__file__).parent / "credentials.db"

conn = sqlite3.connect(dir_db)
cursor = conn.cursor()

cursor.execute("""
    
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    publ_pass TEXT NOT NULL,
                    publ_salt BLOB,
                    priv_pass TEXT,
                    priv_salt BLOB)
                    
                """)

conn.commit()
conn.close()

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


verified_account = False
notes_exists = False
repeated = True

def verify_privates(username, password_priv, password_priv_input):
    """
    Asks the user to enter the password to access private notes.
    Allows up to 5 attempts.
    """

    temp_pass = password_priv_input

    try:
        pass_hash.verify(password_priv, password_priv_input)
        logging.info("Private notes access granted")
        private_cryptography = Cryptography(username=username, password=temp_pass)
        logging.info("Cryptography object for private notes created successfully")
        temp_pass = None  # Removes the plain password for security
        return private_cryptography

    except exceptions.VerifyMismatchError:
        logging.warning("Wrong password entered for private notes")
        return None
       

def create_private(username, priv_pass_input):
    """
    Checks if a password exists for private notes.
    If not, asks for and saves a new one.
    """
    
    private_cryptography = Cryptography(username= username, password=priv_pass_input)
    hashed_password = pass_hash.hash(priv_pass_input)

    dir_db = Path(__file__).parent / "credentials.db"
    with sqlite3.connect(dir_db) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET priv_pass = ? WHERE username = ?", (hashed_password, username))
        conn.commit()

    return private_cryptography


class Cryptography():
    """
    Class for file encryption and decryption.
    """
    def __init__(self, password: str, username):
        self.temp_pass = password
        self.username = username
        self.dir_db = Path(__file__).parent / "credentials.db"
        
        def control_salt(salt_name):
            """
            Checks if the salt exists, creates it if not, otherwise retrieves it.
            """
            
            with sqlite3.connect(self.dir_db) as conn:

                cursor = conn.cursor()
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
        

        with sqlite3.connect(self.dir_db) as conn:

            cursor = conn.cursor()
            cursor.execute("SELECT publ_pass FROM users WHERE username = ?", (self.username,))
            password = cursor.fetchone()[0]

        try:
            pass_hash.verify(password, self.temp_pass)
            self.salt = control_salt("publ_salt")

        except exceptions.VerifyMismatchError:
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

        # Check if the file is empty
        if len(encrypted_data) < 12:
            return ""

        nonce = encrypted_data[:12]
        cipher_text = encrypted_data[12:]

        try:
            decrypted_data = self.aesgcm.decrypt(nonce, cipher_text, None)
            decoded_data = decrypted_data.decode('utf-8', errors='ignore')
            return decoded_data

        except Exception as e:
            logging.error(f"Decryption failed for file {directory}: {str(e)}")
            return "Si \xE8 verificato un errore nella decrittazione dei dati"



class Account:
    """
    Handles user account registration and verification.
    """
    def __init__(self, username, password = None, priv_pass = None):
        self.username = username
        self.password = password
        self.priv_pass = priv_pass
        self.dir_db = Path(__file__).parent / "credentials.db"

    def create_account(self):
        """
        Creates a new account and saves the credentials.
        """

        logging.info(f"Creating account for user: {self.username}")
        credentials = {
            "username": self.username,
            "password": self.password,
            "priv_pass": self.priv_pass
        }

        try:

            with sqlite3.connect(self.dir_db) as conn:

                cursor = conn.cursor()

                cursor.execute("SELECT username FROM users WHERE username = ?", (credentials["username"],))
                existing_user = cursor.fetchone()
                if existing_user:
                    raise UsernameAlreadyExists

                cursor.execute("""
                                INSERT INTO users(username, publ_pass, priv_pass) VALUES (?, ?, ?)""",
                               (credentials["username"], credentials["password"], credentials["priv_pass"]))

                conn.commit()

            directory_users = Path(__file__).parent / "users" 
            directory_users.mkdir(exist_ok=True)
            
            directory_all = directory_users / self.username
            directory_all.mkdir(exist_ok=True)

            directory_logs = directory_all / "logs"  
            directory_logs.mkdir(exist_ok=True)

            directory_all_notes = directory_all / "notes"
            directory_public_notes = directory_all_notes / "public"
            directory_private_notes = directory_all_notes / "private"

            directory_all_notes.mkdir(exist_ok=True)
            directory_public_notes.mkdir(exist_ok=True)
            directory_private_notes.mkdir(exist_ok=True)

            logging.basicConfig(
                 level=logging.DEBUG,
                 handlers = [
                         logging.FileHandler(directory_logs / "file_logs.txt"),
                         logging.StreamHandler()  # In console too
                             ],
                 format='%(asctime)s - %(levelname)s - %(message)s',
                 force = True
            )

            logging.info(f"Account created successfully for user: {self.username}")
            return True

        except UsernameAlreadyExists:
            logging.error(f"Username '{self.username}' already exists.")
            return False



    def sign_in(self):
        """
        User registration procedure.
        """
        password_temp = self.password
        priv_pass_temp = self.priv_pass
        self.password = hash_password(self.password)
        self.priv_pass = hash_password(self.priv_pass)
        verified_account = self.create_account()

        if not verified_account:
            logging.info(f"Account creation failed for user: {self.username}")
            return verified_account, None, None

        logging.info(f"Account registered: {self.username}")
        public_cryptography = Cryptography(password_temp, self.username)
        private_cryptography = Cryptography(priv_pass_temp, self.username)
        password_temp = None
        priv_pass_temp = None
        return verified_account, public_cryptography, private_cryptography
        

    def verify_user(self):
        """
        Verifies user credentials.
        """
        
        try:

            with sqlite3.connect(self.dir_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username, publ_pass FROM users WHERE username = ?", (self.username,))
                credentials = cursor.fetchone()

            credentials = {
                            "username": credentials[0],
                            "password": credentials[1]
                            }

        except TypeError:
            logging.error("Username not found during verification")
            return False, None

        try:
            pass_temp = self.password
            pass_hash.verify(credentials["password"], self.password)
            public_cryptography = Cryptography(pass_temp, self.username)
            pass_temp = None
            return True, public_cryptography
        
        except exceptions.VerifyMismatchError:
            logging.error("Password doesn't match, verification failed")
            return False, None


    def verify_priv_user(self):
        """
        Verify the real identity of the user through the password for private notes.
        """
        
        with sqlite3.connect(self.dir_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT priv_pass FROM users WHERE username = ?", (self.username,))
            result = cursor.fetchone()

        if result is None:
            logging.error(f"User '{self.username}' not found or private password not set.")
            return False, None

        private_password = result[0]
        temp_pass = self.priv_pass

        try:
            pass_hash.verify(private_password, self.priv_pass)
            private_cryptography = Cryptography(temp_pass, self.username)
            return True, private_cryptography

        except exceptions.VerifyMismatchError:
            temp_pass = None
            return False, None
        

class UsernameAlreadyExists(Exception):
    """
    Custom exception for when a username already exists:
    """
    pass

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

    def open_note(self, type_cryptography):
        """
        Opens the notes file, decrypts its content, and re-encrypts it immediately.
        """
        if self.directory.stat().st_size != 0:
            # Decrypt the file content
            text = type_cryptography.decrypt(self.directory)

            # Re-encrypt the file immediately
            with open(self.directory, "w") as file:
                file.write(text)
            type_cryptography.encrypt(self.directory)

            logging.info(f"File {self.directory.name} decrypted and re-encrypted.")
        else:
            text = ""

        return text


    def create(self):
        """
        Creates a new notes file.
        """
        if not os.path.exists(self.directory):
            with open(self.directory, "w"):
                pass

            logging.info(f"File created: {self.directory.name}")
            return True

        else: return False

    def delete(self):
        """
        Deletes a selected notes file.
        """
        
        try:
            os.remove(self.directory)
            logging.info("File correctly deleted")
            return True

        except:
            return False

    def save(self, text, type_cryptography):
        """
        Saves the chenges in the notes file.
        """
        
        with open(self.directory, "w") as file:
            file.write(text)

        type_cryptography.encrypt(self.directory)
        logging.info(f"Saved the file changes: {self.directory.name}")

