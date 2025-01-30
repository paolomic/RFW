import pyuac
import multiprocessing
import time
import winsound
from datetime import datetime, timedelta

from pywinauto import Application

# Import Path - Assudo
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import mouse

import ctypes
import time

import subprocess

COH_SETUP = r'C:\Users\Paolo.Michetti\OneDrive - ION\Desktop\CanDeal evolutionSetup_x64_25_6.0.0d3.exe'


def main():
    """
    Funzione principale eseguita dopo l'elevazione UAC.
    """
    print("Esecuzione con privilegi di amministratore!")
    # Aggiungi qui la tua logica principale
    winsound.Beep(1000, 500)  # Beep di conferma

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Non sono in esecuzione come amministratore. Richiesta elevazione UAC...")

        # Avvia un processo separato per monitorare il dialogo UAC
        #uac_process = multiprocessing.Process(target=monitor_uac_dialog)
        #uac_process.start()

        # Richiedi l'elevazione UAC
        #winsound.Beep(2000, 500)  # Beep prima dell'elevazione
        #pyuac.runAsAdmin()  # Riavvia lo script con privilegi di amministratore
        #winsound.Beep(4000, 500)  # Beep dopo l'elevazione

        # Termina il processo dopo l'elevazione (opzionale)
        #uac_process.terminate()
    
        #metodo runas
        subprocess.run(['runas', '/user:Administrator', COH_SETUP], shell=True, check=True)
        time.sleep(1)  # Attendi un secondo per il processo di avvio


    else:
        # Se siamo già in esecuzione come amministratore, esegui la funzione principale
        main()