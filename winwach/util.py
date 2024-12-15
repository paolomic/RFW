from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.timings import wait_until, TimeoutError
import re
import time

### windows handler thread
import win32gui
import win32con
import win32api
import threading

import pyautogui      # uso di coordinate diretto 


def get_main_window(child):
    current_window = child.parent()
    while current_window and not current_window.is_dialog() and not current_window.is_top_level_window():
        current_window = current_window.parent()
    return current_window

def PrintAppTree(some_item):
  #window = find_single_window("Starting Coherence.*", timeout_sec=1)
  window = get_main_window(some_item)
  window.print_control_identifiers()


def get_main_wnd(title_pattern, timeout_sec=10):
    def _find_matching_windows():
        desktop = Desktop(backend="uia")
        all_windows = desktop.windows()
        matching_windows = [w for w in all_windows 
                           if w.window_text() and 
                           re.match(title_pattern, w.window_text()) ]
        return matching_windows

    try:
        matching_windows = _find_matching_windows()
        
        if len(matching_windows) == 0:
            print(f"get_main_wnd RETRY...")
            
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                matching_windows = _find_matching_windows()
                if matching_windows:
                    break
                time.sleep(0.5)                     # Polling Sleep - migliorabile con Windows Hook
        
        # Time has Gone
        if len(matching_windows) == 0:
            print(f"get_main_wnd: NoResult '{title_pattern}' dopo {timeout_sec} secondi")
            return None
        elif len(matching_windows) > 1:
            print(f"get_main_wnd: MultipleMatch {len(matching_windows)} window che matchano '{title_pattern}':")
            for w in matching_windows:
                print(f"- {w.window_text()}")
            return None
        else:
            # Good
            return matching_windows[0]
            #window_title = matching_windows[0].window_text()
            #app = Application(backend="uia").connect(title=window_title)
            #window = app.window(title=window_title)
            #print(f"get_main_wnd: Connected: '{window_title}'")
            #return app               # or app?
            
    except Exception as e:
        print(f"get_main_wnd Error:: {str(e)}")
        return None


def get_single_child_wnd(root_wnd, title_pattern, timeout_sec=10):
    def _find_matching_childs(wnd_root):
        all_windows = wnd_root.children()
        matching_windows = [w for w in all_windows 
                           if w.window_text() and 
                           re.match(title_pattern, w.window_text()) ]
        return matching_windows

    try:
        matching_windows = _find_matching_childs(root_wnd)
        
        if len(matching_windows) == 0:
            print(f"get_single_child_wnd RETRY...")
            
            start_time = time.time()
            while time.time() - start_time < timeout_sec:
                matching_windows = _find_matching_childs(root_wnd)
                if matching_windows:
                    break
                time.sleep(0.5)                     # Polling Sleep - migliorabile con Windows Hook
        
        # Time has Gone
        if len(matching_windows) == 0:
            print(f"get_single_child_wnd: NoMatch '{title_pattern}' dopo {timeout_sec} secondi")
            return None
        elif len(matching_windows) > 1:
            print(f"get_single_child_wnd: MultipleMatch {len(matching_windows)} window che matchano '{title_pattern}':")
            for w in matching_windows:
                print(f"- {w.window_text()}")
            return None
        else:
            # Good!
            window = matching_windows[0]
            return window
            
    except Exception as e:
        print(f"get_single_child_wnd Error:: {str(e)}")
        return None


