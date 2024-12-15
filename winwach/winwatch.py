import win32gui
import win32con
import win32api
import logging
import ctypes
from ctypes import wintypes
import time
import win32gui
import win32process
import signal
import sys

import util

def signal_handler(sig, frame):
    print('Interruzione rilevata. Chiusura in corso...')
    # Aggiungi qui la logica di pulizia
    WindowTracker.ender=True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# Configura logging
""" logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='windows_tracker.log'
)
 """
def get_window_details(hwnd):
  window_text = win32gui.GetWindowText(hwnd)
  if window_text == "":
    return
        
  hwnd_parent = win32gui.GetParent(hwnd)
  if not hwnd_parent:
    return
  
  parent_text = win32gui.GetWindowText(hwnd_parent) if hwnd_parent else "<no-parent>"

  window_class = win32gui.GetClassName(hwnd)
  window_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
  extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        
  window_type = "Unknown"
  if window_style & win32con.WS_POPUP:
      window_type = "Popup Window"
  elif window_style & win32con.WS_CHILD:
      window_type = "Child Window"
  elif window_style & win32con.WS_OVERLAPPEDWINDOW:
      window_type = "Main Window"

  control_type = "Not a Control"
  
  # Alcuni controlli comuni
  control_classes = {
      "Button": "Pulsante",
      "Edit": "Campo di testo",
      "Static": "Etichetta",
      "ComboBox": "Casella combinata",
      "ListBox": "Elenco",
      "Scrollbar": "Barra di scorrimento",
      "SysTreeView32": "Albero",
      "SysListView32": "Vista a elenco"
  }
  if window_class in control_classes:
      control_type = control_classes[window_class]
  
  result = {
      "###HWND": hwnd,
      "Window Text": window_text,
      "parent hwnd": hwnd_parent,
      "Parent Text": parent_text,
      "Window Class": window_class,
      "Window Type": window_type,
      "Control Type": control_type,
      "Window Style": hex(window_style),
      "Extended Style": hex(extended_style),
  }

  #print (result)
  return result


class WindowTracker:
    ender = False
    pid = 0
    callback=None

    def __init__(self):
        self.user32 = ctypes.windll.user32
        
        # Definisci il prototipo della callback
        self.WinEventProc = ctypes.WINFUNCTYPE(
            None, 
            wintypes.HANDLE, 
            wintypes.DWORD, 
            wintypes.HWND, 
            wintypes.LONG, 
            wintypes.LONG, 
            wintypes.DWORD, 
            wintypes.DWORD
        )

        self.ender = False
        self.callback=None

    def on_window_created(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        try:
          if (not hwnd):
            print("FAIL#1")
            return

          pid = win32process.GetWindowThreadProcessId(hwnd)[1]
          if self.pid!=pid:
            #print("FAIL#2")      # PAre che si ricevano sempre Tutti 
            return
            
          self.callback(hwnd)

          #self.print_window_details(hwnd)
            
          #if window_text == "MyDoc":
           #    self.ender = True        
        
        except Exception as e:
            logging.error(f"Errore nell'acquisizione del testo finestra: {e}")

    def start_tracking(self, callback, pid=0, event="", timeout=60):
        try:
            self.pid = pid
            self.callback = callback
            
            # Crea la callback wrapper
            win_event_proc = self.WinEventProc(self.on_window_created)
            
            # Imposta hook per EVENT_OBJECT_CREATE

            
            if (event == "show"):
               win_event = win32con.EVENT_OBJECT_SHOW
            else:
               win_event = win32con.EVENT_OBJECT_CREATE

            hook = self.user32.SetWinEventHook(
                win_event,
                win_event,
                self.pid,  # Nessun processo specifico
                win_event_proc,
                0,  # Tutti i processi
                0,  # Tutti i thread
                win32con.WINEVENT_OUTOFCONTEXT  # Flag per callback asincrona
            )

            if not hook:
                logging.error("Impossibile impostare il windows hook")
                return

            # Pompa messaggi per mantenere attivo l'hook
            msg = ctypes.wintypes.MSG()
            start = time.time()
            run = 1
            while run:
              
              if time.time() > start+timeout:
                print("TIMEOUT!!!!!")
                run = 0

              if self.ender:
                print("USER BREAK!!!!!")
                run = 0

              while self.user32.PeekMessageA(
                ctypes.byref(msg),  # Puntatore al messaggio
                None,               # Handle finestra (None = tutti)
                0,                  # Filtro min messaggio
                0,                  # Filtro max messaggio
                0x0001              # PM_REMOVE flag
              ) != 0:
                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageA(ctypes.byref(msg))
                
              time.sleep(0.01)

        except KeyboardInterrupt:
            logging.info("Monitoraggio interrotto")
        except Exception as e:
            logging.error(f"Errore nel tracking: {e}")
        
        # Rimuovi hook se impostato
        if 'hook' in locals() and hook:
          self.user32.UnhookWinEvent(hook)


if __name__ == "__main__":
    main()