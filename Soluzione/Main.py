from functions import *
from pathlib import Path
from time import sleep
import logging

# Path to credentials file
credentials_path = Path(__file__).parent / "credentials.json"

# Create credentials.json if it does not exist or is empty
if not credentials_path.exists():
    credentials_path.write_text("{}")
    logging.info("File credentials.json created successfully.")
else:
    if credentials_path.stat().st_size == 0:
        credentials_path.write_text("{}")
        logging.info("File credentials.json existed but was empty, filled with '{}'.")

options = [1, 2, 3, 4]
deleted = False

print("""
                                                    ⚠️ IMPORTANTE ⚠️             
            
                                        DURANTE L'INSERIMENTO DELLA PASSWORD NON 
                                         VERRANNO MOSTRATI I CARATTERI INSERITI 
                                          PER QUESTIONI DI SICUREZZA E PRIVACY
        
        """)

while True:
    verified_account, public_cryptography = verify_user()

    if verified_account:
        repeated = False
        while True:
            sleep(0.5)
            if not repeated:
                print("""Benvenuto in note pad! Cosa vuoi fare? Inserisci il numero corrispondente all'azione che vuoi eseguire:
    1. Scrivere nuovi appunti
    2. Eliminare appunti esistenti
    3. Modificare/leggere appunti esistenti
    4. Esci""")
            else:
                print("""Cosa vorresti fare ora?
    1. Scrivere nuovi appunti
    2. Eliminare appunti esistenti
    3. Modificare/leggere appunti esistenti
    4. Esci""")
            while True:
                try:
                    what_to_do = int(input())
                    if what_to_do not in options:
                        sleep(0.5)
                        print("Inserisci un'opzione valida")
                        logging.critical("Invalid option entered")
                        continue
                    break
                except ValueError:
                    sleep(0.5)
                    print("Inserisci un numero")
                    logging.error("Input error")
                    continue

            if what_to_do == 1:
                sleep(0.5)
                new_notes_name: str = input("Inserisci il nome dei nuovi appunti: ").strip()
                while True:
                    sleep(0.5)
                    private = input("Vuoi rendere questi appunti privati? Saranno protetti da una password (Si/No): ").strip().lower()
                    if private == "si" or private == "sì":
                        notes = FileNotes(directory_private_notes / f"{new_notes_name}.txt")
                        private_cryptography = exists_verify()
                        notes.create(private_cryptography)
                        break
                    elif private == "no":
                        notes = FileNotes(directory_public_notes / f"{new_notes_name}.txt")
                        notes.create(public_cryptography)
                        break
                    else:
                        print("Inserisci una risposta valida")
                        logging.error("Invalid answer entered for note privacy")
                logging.info(f"Note created: {new_notes_name}.txt in {'private' if private in ['si', 'sì'] else 'public'}")

            elif what_to_do == 2:
                sleep(0.5)
                sep_notes_list = [os.listdir(directory_private_notes), os.listdir(directory_public_notes)]
                notes_list_tot = sep_notes_list[0] + sep_notes_list[1]
                if not notes_list_tot:
                    print("Non hai appunti da eliminare")
                    logging.warning("Attempted to delete notes but none exist")
                    sleep(0.5)
                    os.system("cls")
                    continue
                delete_notes()

            elif what_to_do == 3:
                sleep(0.5)
                sep_notes_list = [os.listdir(directory_private_notes), os.listdir(directory_public_notes)]
                notes_list_tot = sep_notes_list[0] + sep_notes_list[1]
                if not notes_list_tot:
                    print("Non hai appunti da leggere o modificare")
                    logging.warning("Attempted to read/modify notes but none exist")
                    sleep(0.5)
                    os.system("cls")
                    continue
                notes_to_open, priv_publ, private_cryptography = notes_considered("da aprire")
                if priv_publ == 1:
                    notes = FileNotes(directory_private_notes / sep_notes_list[0][notes_to_open-1])
                    notes.open(private_cryptography)
                else:
                    notes = FileNotes(directory_public_notes / sep_notes_list[1][notes_to_open-1])
                    notes.open(public_cryptography)
                logging.info("File read/modified successfully")

            elif what_to_do == 4:
                sleep(0.5)
                print("Alla prossima!")
                logging.info("Program exited")
                break

            else:
                if not isinstance(what_to_do, int):
                    print("Inserisci un numero")
                    logging.error("Input error")
                    sleep(0.5)
            os.system("cls")
            repeated = True
    break
