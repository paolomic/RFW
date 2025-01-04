from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto import mouse

import time
import re


## TODO #####################
# 
#  - reload node affidabile 
#


######################################################################################################
# COMMON
######################################################################################################
def is_array(a):
    if isinstance(a, (list, tuple)):
        return True
    return (not isinstance(a, (str, dict)) and hasattr(a, 'iter') and hasattr(a, 'len'))

def array_to_str(arr, sep=' ', max_depth=None, depth=0):
    if max_depth is not None and depth > max_depth:
        return "..."
    if not is_array(arr):
        return str(arr)
    
    return sep.join(array_to_str(elem, sep, max_depth, depth + 1) 
                   for elem in arr)

def all_substr_in(subs:list, thestr:str, case_sens=True):        
    if not is_array(subs):
        if (not case_sens):
            subs.lower()
            thestr.lower()
        return str(subs) in str(thestr)
    return all(all_substr_in(elem, thestr) for elem in subs)
    

######################################################################################################
# WIN
######################################################################################################

def win_move(window, x, y):
  window.iface_transform.Move(x, y)

def win_resize(window, w, h):
  window.iface_transform.Resize(w, h)

def win_activate(window, unminimize = True, wait_end=0.25, wait_restore=0.5):
    window.set_focus()
   
    if unminimize and window.element_info.control_type == 'Window' and window.is_minimized():
        window.restore()
        time.sleep(wait_restore)  # Attende il ripristino
    time.sleep(wait_end)

def win_coord(window, where='c'):
    rect = window.element_info.rectangle
    #altri where
    if where=='c':
        x = (rect.left + rect.right) // 2
        y = (rect.top + rect.bottom) // 2
        return(x,y)   # absolute

def win_click(window, wait_end=0.25):
    rect = window.element_info.rectangle
    click_x = (rect.left + rect.right) // 2
    click_y = (rect.top + rect.bottom) // 2
    window.click_input(coords=(click_x - rect.left, click_y - rect.top))    # usa coord relative
    time.sleep(wait_end)
    return (click_x, click_y)                                               # abs cord

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
def match_value(pattern, value, regex=False, case_sens=True):
    try:          
        if (not case_sens):
            pattern.lower()     # puo essere regexp
            value.lower()
        if regex:
            return bool(re.match(pattern, str(value)))
        return pattern == value
    except Exception:
        return False
  
def check_control(control, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         recursive=False, regex=False, case_sens=True, visible_only=False):
    try:
        if not control.is_enabled():
          return False
        
        if visible_only:
            try:
                if not control.is_visible():
                    return False
            except Exception:
                pass
            
        if name is not None:
            try:
                if not match_value(name, control.window_text(), regex, case_sens):
                    return False
            except Exception:
                return False

        if ctrl_type is not None:
            try:
                if not match_value(ctrl_type, control.element_info.control_type, False, case_sens):
                    return False
            except Exception:
                return False
        
        if class_name is not None:
            try:
                if not match_value(class_name, control.element_info.class_name, False, case_sens):
                    return False
            except Exception:
                return False


        if automation_id is not None:
            try:
                if not match_value(automation_id, control.element_info.automation_id, False, case_sens):
                    return False
            except Exception:
                return False


        if handle is not None:
            try:
                if control.element_info.handle != handle:
                    return False
            except Exception:
                return False

        if texts is not None:
            try:
                properties = control.get_properties()
                prop_texts = properties.get('texts', [])

                if not all_substr_in(texts, array_to_str(prop_texts), case_sens):
                    return False
            except Exception:
                return False      
        
        return True
            
    except Exception:
        return False

def get_child(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         recursive=False, regex=False, case_sens=True, visible_only=False):
    
    if not parent_wnd:
        return None
            
    try:
        # Usa descendants() se recursive=True, altrimenti children()
        elements = parent_wnd.descendants() if recursive else parent_wnd.children()
        
        for element in elements:
            if check_control(element, name, ctrl_type, class_name, automation_id, handle, texts,
                              recursive, regex, case_sens, visible_only):
              return element
                
    except Exception:
        pass
        
    return None

def get_child_retry(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         recursive=False, regex=False, case_sens=True, visible_only=False,
                         attempt=5, wait_init=0.25,  delay=1, wait_end=0.25):
    time.sleep(wait_init)
    while attempt>0:
        #print (attempt)
        cld = get_child(parent_wnd, name, ctrl_type, class_name, automation_id, handle, texts,
                         recursive, regex, case_sens, visible_only)
        if (cld):
            time.sleep(wait_end) 
            return cld
        
        attempt -= 1
        if attempt==0:
            return None
        time.sleep(delay) 

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

def list_select(list_control, value, regex=False):
    list_item = get_child(list_control, name=value, regex=regex)
    
    if (not list_item):
        return False
    win_click(list_item, wait_end=0.5)
    print("click")
    return True


def list_select_texts(list_control, text_values, regex=False):
    list_item = get_child(list_control, texts=text_values, regex=regex)

    if (not list_item):
      return False
    win_click(list_item, wait_end=0.5)
    return True

######################################################################################################
# Dump - (Develop Helpers)
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
        
