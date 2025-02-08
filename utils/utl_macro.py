import keyboard
import threading
import time
from typing import Callable, Dict, List, Union

class MacroManager:
    def __init__(self, repeat_delay: float = 0.05, check_delay: float = 0.05):
        self.macros: Dict[str, tuple[Callable, bool, List[str]]] = {}
        self._running = False
        self.repeat_delay = repeat_delay
        self.check_delay = check_delay

    def set_macro(self, hotkeys: Union[str, List[str]], callback: Callable, repeat: bool = False) -> None:
        """
        Registra una nuova macro.
        Args:
            hotkeys: Singola hotkey o lista di hotkeys (es: ["ctrl", "alt", "1"])
            callback: Funzione da eseguire
            repeat: Se True, ripete la callback mentre le hotkeys sono premute
        """
        if isinstance(hotkeys, str):
            hotkeys = hotkeys.split('+')
            
        if not self.macros:
            keyboard.on_press(self._handle_key_event)
            
        key = " ".join(hotkeys)
        self.macros[key] = (callback, repeat, hotkeys)

    def _check_hotkeys(self, hotkeys: List[str]) -> bool:
        """Verifica se tutte le hotkeys sono premute"""
        return all(keyboard.is_pressed(key) for key in hotkeys)

    def _handle_key_event(self, event):
        if not self._running:
            return

        for _, (callback, repeat, hotkeys) in self.macros.items():
            if self._check_hotkeys(hotkeys):
                if repeat:
                    start_time = time.time()
                    callback()
                    while self._check_hotkeys(hotkeys):
                        if time.time() - start_time >= self.repeat_delay:
                            callback()
                            start_time = time.time()
                        time.sleep(self.check_delay)
                else:
                    callback()
                    while self._check_hotkeys(hotkeys):
                        time.sleep(self.check_delay)
                break

    def start(self):
        self._running = True
    
    def stop(self):
        self._running = False
        keyboard.unhook_all()



""" 
=============================================================================================== KEYS
Tasti standard:
a, b, c, ..., z (lettere minuscole)
A, B, C, ..., Z (lettere maiuscole)
0, 1, 2, ..., 9 (numeri)
!, @, #, $, %, ^, &, *, (, ), -, _, =, +, [, ], {, }, \\, |, ;, :, ', ", ,, <, ., >, /, ?, `, ~ (simboli)

Tasti speciali:
space (barra spaziatrice)
enter (invio)
tab (tabulazione)
backspace (cancellazione)
delete (cancella)
insert (inserisci)
home (inizio)
end (fine)
page up (pagina su)
page down (pagina giù)
up (freccia su)
down (freccia giù)
left (freccia sinistra)
right (freccia destra)
esc (escape)
caps lock (blocco maiuscole)
num lock (blocco numerico)
scroll lock (blocco scorrimento)
print screen (stampa schermo)
pause (pausa)

Tasti funzione:
f1, f2, f3, ..., f12 (tasti funzione da F1 a F12)

Tasti modificatori:
shift (maiuscolo)
ctrl (control)
alt (alternate)
alt gr (alternate graphic)
win (tasto Windows)
cmd (tasto Command su macOS)

Tasti numerici (tastierino numerico):
num 0, num 1, num 2, ..., num 9 (tasti numerici del tastierino numerico)
num lock (blocco numerico)
num / (divisione)
num * (moltiplicazione)
num - (sottrazione)
num + (addizione)
num enter (invio del tastierino numerico)
num . (punto decimale del tastierino numerico)

Combinazioni di tasti:
Puoi anche referenziare combinazioni di tasti, ad esempio:

ctrl + c (copia)
ctrl + v (incolla)
alt + f4 (chiudi la finestra)
shift + a (maiuscolo + A)

"""