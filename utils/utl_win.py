from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto import mouse

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

def win_coord(window, where='c'):
    rect = window.element_info.rectangle
    #altri where
    if where=='c':
      x = (rect.left + rect.right) // 2
      y = (rect.top + rect.bottom) // 2
      return(x,y)   # absolute

def win_click(window, wait=0.1):
    rect = window.element_info.rectangle
    click_x = (rect.left + rect.right) // 2
    click_y = (rect.top + rect.bottom) // 2
    window.click_input(coords=(click_x - rect.left, click_y - rect.top))    # usa coord relative
    time.sleep(wait)
    return (click_x, click_y) #abs

######################################################################################################
# find_window
######################################################################################################
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


######################################################################################################
# get_child
######################################################################################################
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

#TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST 
def win_reload_bytype(item):
    #name = item.window_text()
    #classname = item.element_info.class_name
    ctrltype = item.element_info.control_type

    if ctrltype=='':
      ctrltype=None

    return get_child(item.parent(), ctrl_type=ctrltype)


######################################################################################################
# List
######################################################################################################

def list_select(list_control, s):
    items = list_control.children()
    for item in items:
        
        try:
            properties = item.get_properties()
            text = properties.get('texts', [])
            #text = item.windows_text()

            if(s in text):
              win_click(item)
            
        except Exception as e:
            print(f"Errore nel processare un item: {e}")
            continue


def list_select_texts(list_control, s1=None, s2=None, s3=None):
    items = list_control.children()
    for item in items:
        
        try:
            properties = item.get_properties()
            texts = properties.get('texts', [])



            #xy=win_coord(item)
            #mouse.move(coords=xy)
            #time.sleep(0.1)
            
            # Verifica match posizionale
            found = True
            if s1 is not None and (len(texts) < 1 or s1 not in texts[0]):
                found = False
            if s2 is not None and (len(texts) < 2 or s2 not in texts[1]):
                found = False
            if s3 is not None and (len(texts) < 3 or s3 not in texts[2]):
                found = False
            
            if found:
              win_click(item)
              #item.click_input()
              pass
                
        except Exception as e:
            print(f"Errore nel processare un item: {e}")
            continue
        

######################################################################################################
# Dump
######################################################################################################

def dump_uia_item(element, level=0):
    """
    Converte un elemento UIA in una stringa formattata.
    
    Args:
        element: Elemento UIAWrapper da convertire
        level: Livello di indentazione
    Returns:
        str: Stringa formattata con le proprietà dell'elemento
    """
    try:
        indent = "  " * level
        
        # Raccolta proprietà
        visible = element.is_visible() if hasattr(element, 'is_visible') else None
        control_type = element.element_info.control_type if hasattr(element.element_info, 'control_type') else None
        class_name = element.element_info.class_name if hasattr(element.element_info, 'class_name') else None
        automation_id = element.element_info.automation_id if hasattr(element.element_info, 'automation_id') else None
        window_text = element.window_text() if hasattr(element, 'window_text') else None
        
        # Tentativo di estrarre texts dalle properties
        texts = []
        try:
            properties = element.get_properties()
            texts = properties.get('texts', [])
        except:
            pass
        
        # Costruzione parti dell'output
        output_parts = [
            f"{indent}Level={level}",
            f"Visible={visible}",
            f"Type={control_type}",
            f"Class={class_name}",
            f"AutomationId={automation_id}",
            f"Text='{window_text}'" if window_text else "Text=None",
            f"Texts={texts}" if texts else "Texts=[]"
        ]
        
        return " | ".join(output_parts)
        
    except Exception as e:
        return f"{indent}Error processing element: {str(e)}"

def dump_uia_tree(element, level=0, max_depth=None, file_path='out.txt', first_call=True):
    """
    Stampa l'albero dei controlli su file, una riga per elemento.
    
    Args:
        element: Elemento UIAWrapper da analizzare
        level: Livello corrente di indentazione
        max_depth: Profondità massima dell'albero
        file_path: Percorso del file di output
        first_call: Flag per resettare il file alla prima chiamata
    """
    # Reset file if this is the first call
    mode = 'w' if first_call else 'a'
    
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            # Dump elemento corrente
            f.write(dump_uia_item(element, level) + "\n")
            
            # Processo ricorsivo sui figli
            if max_depth is None or level < max_depth:
                try:
                    children = element.children()
                    for child in children:
                        dump_uia_tree(child, level + 1, max_depth, file_path, False)
                except Exception as e:
                    f.write(f"{'  ' * level}Error getting children: {str(e)}\n")
                    
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        
def dump_uia_path(item, root=None, file_path='out.txt'):
    """
    Stampa il percorso dall'elemento item fino al root (o alla window se root non specificato)
    risalendo con parent().
    
    Args:
        item: Elemento UIAWrapper di partenza
        root: Elemento UIAWrapper di arrivo (opzionale)
        file_path: Percorso del file di output
    """
    try:
        # Raccogli il percorso risalendo con parent()
        path = []
        current = item
        while current is not None:
            path.append(current)
            if root and current == root:
                break
            try:
                current = current.parent()
            except:
                break
                
        # Se root è specificato ma non è stato trovato nel percorso
        if root and path[-1] != root:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Path not found: root element is not an ancestor of item\n")
            return
            
        # Inverti il path per averlo dal root al target
        path.reverse()
        
        # Scrivi il percorso su file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("=== Path from root to target ===\n")
            for level, element in enumerate(path):
                f.write(dump_uia_item(element, level) + "\n")
                
    except Exception as e:
        print(f"Error in dump_uia_path: {str(e)}")       
        
