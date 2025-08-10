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

import json
from time import sleep
import subprocess
import getpass
import logging
from argon2 import PasswordHasher
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

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
    filename=str(directory_logs / "file_logs.log"),
    filemode="a"
)

verified_account = False
notes_exists = False
credentials_exists = False
repeated = True

def verify_privates(credentials_priv):
    """
    Asks the user to enter the password to access private notes.
    Allows up to 5 attempts.
    """
    sleep(0.5)
    print("Abbiamo notato che hai già una password per i file privati! Procedi ad inserirla per accedervi")
    
    for i in range(5):
        password_priv = getpass.getpass("Inserisci la password per gli appunti privati: ")
        temp_pass = password_priv  # Temporarily stores the password for encryption
        try:
            pass_hash.verify(credentials_priv, password_priv)
            sleep(0.5)
            print("Accesso autorizzato")
            logging.info("Private notes access granted")
            private_cryptography = Cryptography(temp_pass)
            logging.info("Cryptography object for private notes created successfully")
            temp_pass = None  # Removes the plain password for security
            sleep(0.5)
            return private_cryptography

        except Exception:
            if i < 4:
                sleep(0.5)
                print("Password errata, accesso rifiutato, riprova")
                logging.warning("Wrong password entered for private notes")
            else:
                sleep(0.5)
                print("Troppi tentativi falliti")
                logging.error("Too many failed attempts for private notes access")
                sleep(0.5)
                exit()

def exists_verify():
    """
    Checks if a password exists for private notes.
    If not, asks for and saves a new one.
    """
    try:
        with open(file_credentials.directory, "r") as file:
            creds = json.load(file)
            priv_pw = creds["password_priv"]
        private_cryptography = verify_privates(priv_pw)
        return private_cryptography
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        priv_pw = getpass.getpass(
            "Password per i file privati non esistente, creane una: "
        ).strip()
        logging.info("Private notes password created successfully")
        temp_pass = priv_pw
        priv_pw = hash_password(priv_pw)
        try:
            with open(file_credentials.directory, "r") as file:
                creds = json.load(file)
            if not isinstance(creds, dict):
                creds = {}
        except (FileNotFoundError, json.JSONDecodeError):
            creds = {}
        creds["password_priv"] = priv_pw
        with open(file_credentials.directory, "w") as file:
            json.dump(creds, file, indent=4)

        logging.info("Private notes password saved successfully")
        print("Nuova password salvata correttamente.")

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
    def __init__(self, password: str):
        self.password = password
        with open(file_credentials.directory, "r") as file:
            credentials = json.load(file)
        def control_salt(salt_name):
            """
            Checks if the salt exists, creates it if not, otherwise retrieves it.
            """
            if salt_name not in credentials:
                salt = secrets.token_bytes(16)
                with open(file_credentials.directory, "w") as file:
                    credentials[salt_name] = salt.hex()
                    json.dump(credentials, file, indent=4)
            else:
                salt = bytes.fromhex(credentials["salt"])
            return salt
        if password == credentials["password"]:
            self.salt = control_salt("pub_salt")
        else:
            self.salt = control_salt("priv_salt")
        self.key = self.derive_key(password, self.salt)
        self.aesgcm = AESGCM(self.key)
        self.password = None  # Removes the plain password for security

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
        with open(file_credentials.directory, "w") as file:
            try:
                already_existing = json.load(file)
                together = already_existing + credentials
                json.dump(together, file, indent=4)
            except:
                json.dump(credentials, file, indent=4)
            logging.info(f"Credentials saved for user: {self.username}")

    def sign_up(self):
        """
        User registration procedure.
        """
        sleep(0.5)
        print("Abbiamo notato che non sei ancora registrato! Procedi a creare un account!")
        sleep(0.5)
        self.username = input("Inserisci il nome utente: ").strip()
        sleep(0.5)
        self.password = getpass.getpass("Inserisci la password: ").strip()
        password_temp = self.password
        self.password = hash_password(self.password)
        self.create_account()
        logging.info(f"Account registered: {self.username}")
        public_cryptography = Cryptography(password_temp)
        password_temp = None
        verified_account = True
        return verified_account, public_cryptography

    def verify_account(self):
        """
        Verifies user credentials.
        """
        with open(file_credentials.directory, "r") as file:
            credentials = json.load(file)
        username_input = input("Inserisci il nome utente: ").strip()
        password_input = getpass.getpass("Inserisci la password: ").strip()
        if username_input != credentials["username"]:
            logging.error("Wrong username entered during account verification")
            return "Credenziali errate"
        try:
            pass_hash.verify(credentials["password"], password_input)
            logging.info("Account successfully verified")
            return "Account verificato!"
        except Exception:
            logging.error("Wrong password entered during account verification")
            return "Credenziali errate"

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

def verify_user():
    """
    Checks if the user is registered and authenticated.
    If not, starts the registration.
    Allows up to 3 login attempts.
    """
    global verified_account
    attempts = 0
    while attempts < 3:
        try:
            with open(file_credentials.directory, "r") as file:
                credentials = json.load(file)
            if not "username" in credentials or not "password" in credentials:
                account = Account("", "")
                verified_account, public_cryptography = account.sign_up()
                sleep(0.5)
                print("Registrazione completata con successo!")
                sleep(0.5)
                os.system("cls")
                return verified_account, public_cryptography
            else:
                if attempts == 0: print("Abbiamo notato che sei già registrato! Procedi a verificare la tua identità!")
                sleep(0.5)
                username_input = input("Inserisci il nome utente: ").strip()
                sleep(0.5)
                password_input = getpass.getpass("Inserisci la password: ").strip()
                public_cryptography = Cryptography(password_input)
                sleep(0.5)
                if username_input != credentials["username"]:
                    raise VerifyError()
                try:
                    pass_hash.verify(credentials["password"], password_input)
                except Exception:
                    public_cryptography = None
                    raise VerifyError()
                print("Account verificato con successo!")
                logging.info("Account successfully verified")
                sleep(0.5)
                os.system("cls")
                verified_account = True
                return verified_account, public_cryptography
        except VerifyError:
            attempts += 1
            print("Nome utente o password non validi. Account non verificato")
            logging.error("Wrong username or password entered during account verification")
            if attempts == 3:
                print("Troppi tentativi falliti. Uscita dal programma.")
                logging.error("Too many failed attempts for account verification")
                exit()
        except FileNotFoundError:
            account = Account("", "")
            account.sign_up()
            verified_account = True
            return verified_account, public_cryptography

class File:
    """
    Base class for file management.
    """
    def __init__(self, directory):
        self.directory = directory

class FileCredentials(File):
    """
    Manages the credentials file.
    """
    def __init__(self, directory):
        global credentials_exists
        super().__init__(directory)
        if self.directory == Path(__file__).parent / "credentials.json":
            try:
                with open(self.directory, "r") as file:
                    self.data = json.load(file)
                credentials_exists = True
            except (FileNotFoundError, json.JSONDecodeError):
                self.data = None

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

# Global object for credentials management
file_credentials = FileCredentials(Path(__file__).parent / "credentials.json")

