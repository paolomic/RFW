
import keyboard
from pywinauto.keyboard import send_keys
import time

# import da altri path - 
import sys
from pathlib import Path
path_utl = str(Path(__file__).parent.parent)
sys.path.append(path_utl)

import utl_macro



macro_mgr = utl_macro.MacroManager(
      repeat_delay=0.1,    # Tempo tra le ripetizioni
      check_delay=0.05     # Tempo di sleep nei cicli
  )
    
def write_x():
    send_keys('x')
    
def write_hello():
    send_keys('Hello World!')

# Registra le macro
macro_mgr.set_macro('ctrl alt 1', write_x, repeat=True)
macro_mgr.set_macro("ctrl alt 2", write_hello, repeat=False)

# Avvia
macro_mgr.start()

print("Macro Manager attivo. CPU ottimizzata.")
print("CTRL+ALT+1 - scrive 'x' (repeat)")
print("CTRL+ALT+2 - scrive 'Hello World!'")
print("Ctrl+C per terminare")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    macro_mgr.stop()
    print("\nTerminato.")
