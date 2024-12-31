from pywinauto.keyboard import send_keys
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
            hotkeys = hotkeys.split()
            
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