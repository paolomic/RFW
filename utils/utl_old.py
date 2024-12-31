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

import pyautogui      # uso di coordinate diretto Altro wapper !!!

#################################################################

def get_main_window(child):
    current_window = child.parent()
    while current_window and not current_window.is_dialog() and not current_window.is_top_level_window():
        current_window = current_window.parent()
    return current_window

def PrintAppTree(some_item):
  #window = find_single_window("Starting Coherence.*", timeout_sec=1)
  window = get_main_window(some_item)
  window.print_control_identifiers()

def click_popup_menu_item(some_item, menu_item_text):
  try:
    main_window = get_main_window(some_item)
    all_popmenu_items = main_window.descendants(
        title="PopupMenu", 
        control_type="Menu"
    )
    all_menu_items = all_popmenu_items[0].descendants(
        title=menu_item_text, 
        control_type="MenuItem"
    )
    if all_menu_items:
        all_menu_items[0].click_input()
    else:
        print(f"Elemento {menu_item_text} non trovato nel popup menu")
  except Exception as e:
    print(f"Errore nella selezione dell'elemento {menu_item_text}: {e}")

def toggle_list_item(list_control, item_text):
  try:
      # Trova i ListItem con il testo specificato
      list_items = list_control.descendants(
          title=item_text, 
          control_type="ListItem"
      )
      
      # Esegui il toggle
      if list_items:
          list_item = list_items[0]
          # Prova a usare click_input() con coordinate precise
          list_item.click_input(coords=(5, 5))
      else:
          print(f"ListItem {item_text} non trovato")

  except Exception as e:
      print(f"Errore nel toggle dell'elemento {item_text}: {e}")

def get_list_item_toggle_state(list_control, item_text):
    try:
        # Trova i ListItem con il testo specificato
        list_items = list_control.descendants(
            title=item_text, 
            control_type="ListItem"
        )
        
        # Restituisce lo stato di toggle
        if list_items:
            # Usa il primo elemento trovato
            xxx = str(list_items[0])
            yyy = list_items.get_toggle_state()
            return True if 'Checked' in xxx else False
        else:
            print(f"ListItem {item_text} non trovato")
            return None
    
    except Exception as e:
        print(f"Errore nel recupero dello stato di toggle per {item_text}: {e}")
        return None
    
def list_check_mass(list_ctrl, mode):
  header_ctrl = list_ctrl.child_window(control_type="Header")
  try:
    rect = header_ctrl.rectangle()
    x = rect.left +7
    y = rect.top +7
    pyautogui.rightClick(x, y)
    time.sleep(0)
    #PrintAppTree()
    click_popup_menu_item(list_ctrl, "Check all" if mode=="*" else "Uncheck all")
  except:
    pass

def list_check(list_ctrl, rowkey):
  for list_item in list_ctrl.items():
    child = list_item.children()[0]
    try:
        text = child.window_text()
        if (text==rowkey):
          rect = child.rectangle()
          checkbox_x = rect.left - 10
          checkbox_y = rect.top + 7
          pyautogui.click(checkbox_x, checkbox_y)
    except:
        pass



def listbox_to_json(listbox_window):
    # Estrai gli header
    headers = []
    header_control = listbox_window.child_window(control_type="Header")
    for header in header_control.children():
        try:
            text = header.window_text()
            if text != "":  # Aggiunto per escludere header vuoti
                headers.append(text)
        except:
            pass
    
    # Estrai i dati delle righe
    rows = []
    for list_item in listbox_window.items():
        row_data = {}
        
        # Prendi i figli di ogni ListItem (Static text)
        static_texts = []
        for child in list_item.children():
            try:
                # Prova a usare window_text() per tutti i figli
                text = child.window_text()
                static_texts.append(text)
            except:
                pass
        
        # Associa i campi agli header 
        # Salta la prima riga se corrisponde agli header
        if static_texts != headers:
            for i, header in enumerate(headers):
                if i < len(static_texts):
                    row_data[header] = static_texts[i]
            
            rows.append(row_data)
    return rows


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
            # Good
            window = matching_windows[0]
            return window
            
    except Exception as e:
        print(f"get_single_child_wnd Error:: {str(e)}")
        return None

