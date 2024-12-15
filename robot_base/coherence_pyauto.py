import subprocess
import time
from pywinauto.application import Application

def test_coherence():
    # Avvia l'applicazione
    app = Application(backend="uia").start(r"D:\COH_x64_CANDEAL_NEXT\bin\Coherence.exe")
    
    # Attendi che la finestra principale appaia
    time.sleep(5)  # Attesa base di 5 secondi
    
    # Trova la finestra principale
    main_window = app.window(title="Starting Coherence [DEBUG version]")
    
    # Clicca il pulsante Open
    main_window.child_window(title="Open", auto_id="1", control_type="Button").click()

if __name__ == "__main__":
    test_coherence()