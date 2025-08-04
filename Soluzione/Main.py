from funzioni import *
from pathlib import Path
from time import sleep
import logging

credenziali_path = Path(__file__).parent / "credenziali.json"

if not credenziali_path.exists():
    credenziali_path.write_text("{}")
    logging.info("File credenziali.json creato con successo.")
else:
    # Se il file esiste ma è vuoto, scrivi "{}"
    if credenziali_path.stat().st_size == 0:
        credenziali_path.write_text("{}")
        from funzioni import *
        from pathlib import Path
        from time import sleep
        import logging

        credenziali_path = Path(__file__).parent / "credenziali.json"

        if not credenziali_path.exists():
            credenziali_path.write_text("{}")
            logging.info("File credenziali.json creato con successo.")
        else:
            if credenziali_path.stat().st_size == 0:
                credenziali_path.write_text("{}")
                logging.info("File credenziali.json esistente ma vuoto, riempito con '{}'.")

opzioni = [1, 2, 3, 4]
eliminato = False

print("""
                                                    ⚠️ IMPORTANTE ⚠️             
            
                                        DURANTE L'INSERIMENTO DELLA PASSWORD NON 
                                         VERRANNO MOSTRATI I CARATTERI INSERITI 
                                          PER QUESTIONI DI SICUREZZA E PRIVACY
        
        """)

while True:
    
    account_verificato = verifica_utente()

    if account_verificato:
        ripetuto = False
        while True:
            
            sleep(0.5)
            
            if not ripetuto:            
                print("""Benvenuto in note pad! Cosa vuoi fare? Inserisci il numero corrispondente all'azione che vuoi eseguire:
    1. Scrivere nuovi appunti 
    2. Eliminare appunti esistenti 
    3. modificare/leggere appunti esistenti
    4. Esci""")
                
            else:
                print("""Cosa vorresti fare ora?
    1. Scrivere nuovi appunti 
    2. Eliminare appunti esistenti 
    3. Modificare/leggere appunti esistenti
    4. Esci""")
                
            while True:
                try:    
                    cosa_fare = int(input())

                    if cosa_fare not in opzioni:
                        print("Inserisci un opzione valida")
                        logging.critical("Opzione non valida inserita")
                        continue
                    
                    break

                except ValueError:
                    sleep(0.5)
                    print("Inserisci un numero")
                    logging.error("Errore di input")
                    continue
            

            if cosa_fare == 1:
                sleep(0.5)
                nome_nuovi_appunti: str = input("Inserisci il nome dei nuovi appunti: ").strip()
                
                while True:
                    
                    privato = input("Vuoi rendere questi appunti privati? Saranno protetti da una password(Si/No): ").strip().lower()                
                        
                    if privato == "si" or privato == "sì":
                        appunti = FileAppunti(directory_appunti_privati / f"{nome_nuovi_appunti}.txt")
                        appunti.crea()
                        break
                        
                    elif privato == "no":
                        appunti = FileAppunti(directory_appunti_pubblici / f"{nome_nuovi_appunti}.txt")
                        appunti.crea()
                        break
                            
                    else:
                        print("Inserisci una risposta valida")
                        logging.error("Risposta non valida inserita per la privacy degli appunti")

                logging.info(f"Appunti creati: {nome_nuovi_appunti}.txt in {'privati' if privato in ['si', 'sì'] else 'pubblici'}")
                    
                
            
            elif cosa_fare == 2:
                sleep(0.5)
                
                lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
                lista_appunti_tot = lista_appunti_sep[0] + lista_appunti_sep[1]

                if not lista_appunti_tot: print("Non hai appunti da eliminare"); logging.warning("Tentativo di eliminazione appunti ma nessuno presente"); continue

                elimina_appunti()
                
            elif cosa_fare == 3:
                sleep(0.5)
                
                lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
                lista_appunti_tot = lista_appunti_sep[0] + lista_appunti_sep[1]
                
                if not lista_appunti_tot: print("Non hai appunti da leggere o modificare"); logging.warning("Tentativo di modifica/lettura appunti ma nessuno presente") ; continue
                
                appunti_da_aprire, priv_publ = appunti_considerati("da aprire")
                
                if priv_publ == 1:
                    appunti = FileAppunti(directory_appunti_privati / lista_appunti_sep[0][appunti_da_aprire-1])
                    
                else:
                    appunti = FileAppunti(directory_appunti_pubblici / lista_appunti_sep[1][appunti_da_aprire-1])

                appunti.apri()
                logging.info(f"Lettura/modifica del file andata a buon fine")
            
            elif cosa_fare == 4:
                sleep(0.5)
                print("Alla prossima!")
                logging.info("Uscita dal programma")
                break

            else:
                if not isinstance(cosa_fare, int): print("Inserisci un numero"); logging.error("Errore di input"); sleep(0.5)
                
            os.system("cls")
            ripetuto = True
    break       