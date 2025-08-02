from funzioni import *
from pathlib import Path
from time import sleep

credenziali_path = Path(__file__).parent / "credenziali.json"

if not credenziali_path.exists():
    credenziali_path.write_text("{}")
else:
    # Se il file esiste ma è vuoto, scrivi "{}"
    if credenziali_path.stat().st_size == 0:
        credenziali_path.write_text("{}")

os.makedirs(directory_tutti_gli_appunti, exist_ok=True)
os.makedirs(directory_appunti_pubblici, exist_ok=True)
os.makedirs(directory_appunti_privati, exist_ok=True)

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
        while True:
            
            sleep(0.5)
            
            if not ripetuto:            
                print("""Benvenuto in note pad! Cosa vuoi fare? Inserisci il numero
    1. Scrivere nuovi appunti 
    2. Eliminare appunti esistenti 
    3. modificare/leggere appunti esistenti""")
                
            else:
                print("""Cosa vorresti fare ora?
    1. Scrivere nuovi appunti 
    2. Eliminare appunti esistenti 
    3. Modificare/leggere appunti esistenti
    4. Esci""")
                
            while True:
                try:    
                    cosa_fare = int(input())
                    break
                
                except ValueError:
                    sleep(0.5)
                    print("Inserisci un numero")
                
             
            if cosa_fare not in opzioni:
                print("Inserisci un opzione valida")
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
                    
                
            
            elif cosa_fare == 2:
                sleep(0.5)
                
                lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
                
                if not any([lista_appunti_sep[0], lista_appunti_sep[1]]):
                    print("Non hai appunti da eliminare")
                    continue
            
                elimina_appunti()
                
            elif cosa_fare == 3:
                sleep(0.5)
                
                lista_appunti_sep = [os.listdir(directory_appunti_privati), os.listdir(directory_appunti_pubblici)]
                lista_appunti_tot = lista_appunti_sep[0] + lista_appunti_sep[1]
                
                if not lista_appunti_tot:
                    print("Non hai appunti da leggere o modificare")
                    continue
                
                appunti_da_aprire, priv_publ = appunti_considerati("da aprire")
                
                if priv_publ == 1:
                    appunti = FileAppunti(directory_appunti_privati / lista_appunti_sep[0][appunti_da_aprire-1])
                    
                else:
                    appunti = FileAppunti(directory_appunti_pubblici / lista_appunti_sep[1][appunti_da_aprire-1])

                appunti.apri()
            
            elif cosa_fare == 4:
                sleep(0.5)
                print("Alla prossima!")
                break
                
            ripetuto = True
    break       