import win32gui
import win32con
import win32api
import logging
import ctypes
from ctypes import wintypes


# Configura logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='windows_tracker.log'
)

class WindowTracker:
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

    def on_window_created(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        try:
            # Recupera il testo della finestra
            window_text = win32gui.GetWindowText(hwnd)
            
            # Controlla se il testo contiene la frase chiave e se il titolo è "Coherence"
            hwin_parent = win32gui.GetParent(hwnd)
            if "Do you want to close current workspace?" in window_text and win32gui.GetWindowText(hwin_parent) == "Coherence":
            #if win32gui.GetWindowText(win32gui.GetParent(hwnd)) == "Coherence":
                logging.info(f"Popup Coherence rilevato: '{window_text}'")
                print(f"Popup Coherence rilevato: '{window_text}'")

                ok_button = win32gui.FindWindowEx(hwin_parent, None, None, "OK")
                if ok_button:
                    win32api.PostMessage(ok_button, win32con.WM_LBUTTONDOWN, 0, 0)
                    win32api.PostMessage(ok_button, win32con.WM_LBUTTONUP, 0, 0)
                    logging.info("Pulsante OK premuto automaticamente")
        
        
        except Exception as e:
            logging.error(f"Errore nell'acquisizione del testo finestra: {e}")

    def start_tracking(self):
        try:
            # Crea la callback wrapper
            win_event_proc = self.WinEventProc(self.on_window_created)
            
            # Imposta hook per EVENT_OBJECT_CREATE
            hook = self.user32.SetWinEventHook(
                win32con.EVENT_OBJECT_CREATE,  # Evento di creazione oggetto
                win32con.EVENT_OBJECT_CREATE,  # Stesso evento (range singolo)
                0,  # Nessun processo specifico
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
            while self.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0) != 0:
                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageA(ctypes.byref(msg))

        except KeyboardInterrupt:
            logging.info("Monitoraggio interrotto")
        except Exception as e:
            logging.error(f"Errore nel tracking: {e}")
        finally:
            # Rimuovi hook se impostato
            if 'hook' in locals() and hook:
                self.user32.UnhookWinEvent(hook)

def main():
    print("Avvio tracker popup Coherence. Premi Ctrl+C per interrompere.")
    tracker = WindowTracker()
    tracker.start_tracking()

if __name__ == "__main__":
    main()