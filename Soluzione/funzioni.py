from pathlib import Path
import json
import os
from time import sleep
import subprocess
import getpass

# Directory principali per la gestione degli appunti
directory_tutti_gli_appunti = Path(__file__).parent / "appunti"
directory_appunti_pubblici = directory_tutti_gli_appunti / "pubblici"
directory_appunti_privati = directory_tutti_gli_appunti / "privati"

account_verificato = False
appunti_esistenti = False
credenziali_esistenti = False
ripetuto = True


def verifica_privati(credenziali_priv):
    """
    Chiede all'utente di inserire la password per accedere agli appunti privati.
    Permette fino a 5 tentativi.
    """
    print("Abbiamo notato che hai già una password per i file privati! Procedi ad inserirla per accedervi")
    
    for i in range(5):
        password_priv = getpass.getpass()
        
        if password_priv == credenziali_priv:
            sleep(0.5)
            print("Accesso autorizzato")
            return True
        else:
            if i < 4:
                print("Password errata, accesso rifiutato, riprova")
            else:
                sleep(0.5)
                print("Troppi tentativi falliti")
                exit()


def verifica_esistenza():
    """
    Verifica se esiste una password per gli appunti privati.
    Se non esiste, la richiede e la salva.
    """
    try:
        with open(file_credenziali.directory, "r") as file:
            creds = json.load(file)
            pw_priv = creds["password_priv"]
            
        verifica_privati(pw_priv)
        return pw_priv
    
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Richiede una nuova password se non esiste
        pw_priv = getpass.getpass(
            "Password per i file privati non esistente, creane una: "
        ).strip()
        
        try:
            with open(file_credenziali.directory, "r") as file:
                creds = json.load(file)
                
            if not isinstance(creds, dict):
                creds = {}
                
        except (FileNotFoundError, json.JSONDecodeError):
            creds = {}
            
        creds["password_priv"] = pw_priv
        
        with open(file_credenziali.directory, "w") as file:
            json.dump(creds, file, indent=4)
            
        print("Nuova password salvata correttamente.")
        return pw_priv


def appunti_considerati(del_mod):
    """
    Mostra la lista degli appunti (privati e pubblici) e chiede all'utente quale vuole considerare.
    Argomenti:
        del_mod: stringa che indica l'azione (es. 'da eliminare', 'da aprire')
    Ritorna:
        (indice appunto scelto, tipo appunto: 1=privato, 2=pubblico)
    """
    lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
    lista_appunti_tot = lista_appunti_sep[0] + lista_appunti_sep[1]
    secondo_giro = False

    for a in lista_appunti_sep:
        print("Appunti privati:") if secondo_giro is False else print("Appunti pubblici:")
        conto = 1
        
        for i in a:
            print(f"    {conto}. {i[:-4]}")
            conto += 1
            lista_appunti_tot.append(i)
        secondo_giro = True

    # Richiesta input con ciclo finché non valido
    while True:
        try:
            sleep(0.5)
            priv_publ = int(input(f"""Inserisci il numero dello stato degli appunti {del_mod}:
    1. Privati
    2. Pubblici
"""))
            if priv_publ < 1 or priv_publ > 2:
                sleep(0.5)
                print("Inserisci un numero valido")
            else:
                if priv_publ == 1:
                    verifica_esistenza()
                break
        
        except ValueError:
            sleep(0.5)
            print("Inserisci un numero!")

        print(f"Inserisci il numero corrispondente agli appunti {del_mod}:")
    
    conto = 1
    
    for i in lista_appunti_sep[priv_publ-1]:
        print(f"    {conto}. {i[:-4]}")
        conto += 1

    appunti_da_considerare = None
    while True:
        try:
            appunti_da_considerare = int(input())
            
            if 1 <= appunti_da_considerare <= len(lista_appunti_sep[priv_publ-1]): break
            else: print("Numero non valido, riprova.")
                
        except ValueError:
            print("Inserisci un numero valido.")

    return appunti_da_considerare, priv_publ


def elimina_appunti():
    """
    Gestisce la procedura di eliminazione di un appunto scelto dall'utente.
    """
    lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
    
    appunti_da_eliminare, priv_publ = appunti_considerati("da eliminare")
    
    if priv_publ == 1:
        appunti = FileAppunti(directory_appunti_privati/lista_appunti_sep[0][appunti_da_eliminare-1])
        appunti.elimina(lista_appunti_sep[0], appunti_da_eliminare-1, directory_appunti_privati)
    
    else:
        appunti = FileAppunti(directory_appunti_pubblici/lista_appunti_sep[1][appunti_da_eliminare-1])
        appunti.elimina(lista_appunti_sep[1], appunti_da_eliminare-1, directory_appunti_pubblici)


class File:
    """
    Classe base per la gestione dei file.
    """
    def __init__(self, directory):
        self.directory = directory


class FileCredenziali(File):
    """
    Gestisce il file delle credenziali.
    """
    def __init__(self, directory):
        
        global credenziali_esistenti
        super().__init__(directory)
        
        if self.directory == Path(__file__).parent / "credenziali.json":
            try:
                with open(self.directory, "r") as file:
                    self.dati = json.load(file)
                credenziali_esistenti = True
            except (FileNotFoundError, json.JSONDecodeError): self.dati = None
                

class FileAppunti(File):
    """
    Gestisce i file degli appunti (privati/pubblici).
    """
    def __init__(self, directory):
        super().__init__(directory)
        
        
    def apri(self):
        """
        Apre il file degli appunti con Notepad e segnala eventuali modifiche.
        """
        processo = subprocess.Popen(["notepad.exe", self.directory])
        ultima_modifica = os.path.getmtime(self.directory)
        
        while processo.poll() is None:
            sleep(0.5)
            nuova_modifica = os.path.getmtime(self.directory)
            
            if nuova_modifica != ultima_modifica:
                print("Il file è stato modificato")
                ultima_modifica = nuova_modifica
                
                
    def crea(self):
        """
        Crea un nuovo file di appunti e lo apre.
        """
        with open(self.directory, "w") as file:
            file.write("Scrivi i tuoi appunti qui")
        print("File creato correttamente!")
        sleep(0.5)
        self.apri()
        
        
    def elimina(self, lista_appunti, appunti_da_eliminare, directory_considerata):
        """
        Elimina un file di appunti selezionato.
        """
        global eliminato
        
        for i in lista_appunti:
            
            if lista_appunti[appunti_da_eliminare] == i:
                os.remove(directory_considerata / i)
                print("Appunti eliminati correttamente!")
                eliminato = True
                
        if not eliminato:
            print("Numero non valido")
            

# Oggetto globale per la gestione delle credenziali
file_credenziali = FileCredenziali(Path(__file__).parent / "credenziali.json")


class Account:
    """
    Gestisce la registrazione e la verifica dell'account utente.
    """
    def __init__(self, nome_utente, password):
        self.nome_utente = nome_utente
        self.password = password
        
        
    def crea_account(self):
        """
        Crea un nuovo account e salva le credenziali.
        """
        credenziali = {
            "nome_utente": self.nome_utente,
            "password": self.password
        }
        
        with open(file_credenziali.directory, "w") as file:
            try:
                già_presenti = json.load(file)
                insieme = già_presenti + credenziali
                json.dump(insieme, file, indent=4)
            except:
                json.dump(credenziali, file, indent=4)
                
                
    def registrazione(self):
        """
        Procedura di registrazione di un nuovo utente.
        """
        print("Abbiamo notato che non sei ancora registrato!")
        sleep(0.5)
        self.nome_utente = input("Inserisci il nome utente: ").strip()
        
        sleep(0.5)
        self.password = getpass.getpass("Inserisci la password: ").strip()
        self.crea_account()
        
        account_verificato = True
        return account_verificato
    
    
    def verifica_account(self):
        """
        Verifica le credenziali dell'utente.
        """
        with open(file_credenziali.directory, "r") as file:
            credenziali = json.load(file)
            
        if str(input("Inserisci il nome utente ")) == credenziali["nome_utente"] and str(input("Inserisci la password ")) == credenziali["password"]:
            return "Account verificato!"
        else:
            return "Credenziali errate"


class ErroreVerifica(Exception):
    """
    Eccezione personalizzata per errori di verifica account.
    """
    pass


def verifica_utente():
    """
    Verifica se l'utente è registrato e autenticato.
    Se non lo è, avvia la registrazione.
    Permette fino a 3 tentativi di login.
    """
    global account_verificato
    tentativi = 0
    while tentativi < 3:
        try:
            with open(file_credenziali.directory, "r") as file:
                credenziali = json.load(file)
                
            if not "nome_utente" in credenziali or not "password" in credenziali:
                account = Account("", "")
                account.registrazione()
                account_verificato = True
                sleep(0.5)
                print("Registrazione completata con successo!")
                return account_verificato
            
            else:
                account = Account(credenziali["nome_utente"], credenziali["password"])
                print("Abbiamo notato che sei già registrato! Procedi a verificare la tua identità!")
                sleep(0.5)
                
                nome_utente_input = input("Inserisci il nome utente: ").strip()
                sleep(0.5)
                
                password_input = getpass.getpass("Inserisci la password: ").strip()
                sleep(0.5)
                
                if nome_utente_input != str(credenziali["nome_utente"]) or password_input != str(credenziali["password"]):
                    raise ErroreVerifica()
                
                print("Account verificato con successo!")
                account_verificato = True
                return account_verificato
            
        except ErroreVerifica:
            tentativi += 1
            print("Nome utente o password non validi. Account non verificato")
            
            if tentativi == 3:
                print("Troppi tentativi falliti. Uscita dal programma.")
                exit()
                
        except FileNotFoundError:
            account = Account("", "")
            account.registrazione()
            account_verificato = True
            return account_verificato