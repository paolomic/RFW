from pywinauto.application import Application
from pywinauto import Desktop

import time
import re

def win_move(window, x, y):
  window.iface_transform.Move(x, y)

def win_resize(window, w, h):
  window.iface_transform.Resize(w, h)

def win_activate(window, unminimize = True):
   window.set_focus()
   time.sleep(0.1)
   if unminimize and window.element_info.control_type == 'Window' and window.is_minimized():
      window.restore()
      time.sleep(0.5)  # Attende il ripristino

def win_clickon(window, wait=0.1):
    rect = window.element_info.rectangle
    click_x = (rect.left + rect.right) // 2
    click_y = (rect.top + rect.bottom) // 2
    window.click_input(coords=(click_x - rect.left, click_y - rect.top))
    time.sleep(wait)


def find_window(name=None, class_name=None, handle=None, process_id=None, exact_match=False):
    """
    Trova una finestra di primo livello basata sui criteri specificati.
    
    Args:
        name: Nome/titolo della finestra
        class_name: Nome della classe
        handle: Handle Windows
        process_id: ID del processo
        exact_match: Se True, richiede match esatto per le stringhe
    """
    try:
        desktop = Desktop(backend='uia')
        top_windows = desktop.windows()
        
        for window in top_windows:
            try:
                # Handle check (più veloce)
                if handle is not None:
                    if window.element_info.handle != handle:
                        continue
                
                # Process ID check
                if process_id is not None:
                    if window.process_id() != process_id:
                        continue
                
                # Class name check
                if class_name is not None:
                    try:
                        if window.element_info.class_name != class_name:
                            continue
                    except:
                        continue
                
                # Window name check (potenzialmente più lento)
                if name is not None:
                    try:
                        window_text = window.window_text()
                        if exact_match:
                            if window_text != name:
                                continue
                        else:
                            if name.lower() not in window_text.lower():
                                continue
                    except:
                        continue
                
                return window
                
            except Exception:
                continue
                
        return None
        
    except Exception as e:
        print(f"Error in find_window: {str(e)}")
        return None

def get_child(parent_wnd, name=None, ctrl_type=None, class_name=None, 
              automation_id=None, handle=None, use_regex=False, recursive=False,
              visible_only=False):
    """
    Trova un controllo figlio basato su più criteri.
    Usa descendants() per ricerca ricorsiva, children() altrimenti.
    """
    if not parent_wnd:
        return None

    def match_value(pattern, value):
        try:
            if not value:
                return False
                
            if use_regex:
                return bool(re.match(pattern, str(value)))
            return pattern == value
        except Exception:
            return False
            
    def check_control(control):
        try:
            if not control.is_enabled():
              return False
            
            if visible_only:
                try:
                    if not control.is_visible():
                        return False
                except Exception:
                    pass
            
            if handle is not None:
                try:
                    if control.element_info.handle != handle:
                        return False
                except Exception:
                    return False
            
            if ctrl_type is not None:
                try:
                    if not match_value(ctrl_type, control.element_info.control_type):
                        return False
                except Exception:
                    return False
            
            if class_name is not None:
                try:
                    if not match_value(class_name, control.element_info.class_name):
                        return False
                except Exception:
                    return False
            
            if automation_id is not None:
                try:
                    if not match_value(automation_id, control.element_info.automation_id):
                        return False
                except Exception:
                    return False
            
            if name is not None:
                try:
                    if not match_value(name, control.window_text()):
                        return False
                except Exception:
                    return False
            
            return True
                
        except Exception:
            return False
    
    try:
        # Usa descendants() se recursive=True, altrimenti children()
        elements = parent_wnd.descendants() if recursive else parent_wnd.children()
        
        for element in elements:
            if check_control(element):
                return element
                
    except Exception:
        pass
        
    return None

