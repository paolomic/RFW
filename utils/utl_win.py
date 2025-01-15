from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto import mouse
import keyboard
from datetime import datetime
import time
import re
import win32clipboard

from win32gui import FindWindow, PostMessage
import win32.lib.win32con as win32con

## TODO #####################
# 
#  - reload node affidabile 
#

WIN_BUTT_STATE_CHECKED          = (1<<4)

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
    
def hide_select(n):
    if n>0:
        keyboard.press("home")
        for i in range(0,n-1):
            keyboard.press("down")
    else:
        keyboard.press("end")
        for i in range(0,-n-1):
            keyboard.press("up")

def statusbar_wait(statusbar, state, attempt=5, wait_init=0.25,  delay=1, wait_end=0.25):
    time.sleep(wait_init)
    while attempt>0:
        cld = get_child(statusbar, name=state, ctrl_type='Text')
        if (cld):
            time.sleep(wait_end) 
            return True
        
        attempt -= 1
        if attempt==0:
            return None
        time.sleep(delay) 
    return False

def edit_set(edit, value):
    edit.iface_value.SetValue(value)

def get_today_iso():
  return datetime.now().strftime('%Y%m%d')

def get_log_path(wsp_path, logname):
  filename = f'{logname}_{get_today_iso()}.log'
  return f'{wsp_path}_wrk\\Logs\\{filename}'

######################################################################################################
# WIN
######################################################################################################

def win_close(handle: int):
    PostMessage(handle, win32con.WM_CLOSE, 0, 0)

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

def win_click(window, mode="center", wait_end=0.25, arg=None):        
    rect = window.element_info.rectangle
    click_x = 0
    click_y = 0
    if (mode=='center'):
        click_x = (rect.left + rect.right) // 2
        click_y = (rect.top + rect.bottom) // 2
        
    if (mode=='combo'):
        click_x = (rect.right) -10
        click_y = (rect.top + rect.bottom) // 2

    if (mode=='grid_tl'):
        click_x = (rect.left +10)
        click_y = (rect.top + 10) 

    if (mode=='grid_row1'):
        click_x = (rect.left +30)
        click_y = (rect.top + 26) 
    
    if (mode=='grid_row'):
        click_x = (rect.left +10)
        click_y = (rect.top + 10+(18*arg)) 

    if (mode=='grid_col1'):
        click_x = (rect.left +30)
        click_y = (rect.top + 10) 

    window.click_input(coords=(click_x - rect.left, click_y - rect.top))    # usa coord relative
    time.sleep(wait_end)
    return (click_x, click_y)                                               # abs cord

######################################################################################################
# Grid
######################################################################################################

def grid_select_all(grid):
    win_click(grid, mode='grid_col1')
    win_click(grid, mode='grid_tl')

def grid_select_rows(grid, num, page =False, home=True):
    if num==0:
        return grid_select_all(grid)
    if(home):
        win_click(grid)
        keyboard.press_and_release('ctrl+home')
    win_click(grid, mode='grid_row', arg=1)
    keyboard.press('shift')
    #win_click(grid, mode='grid_row', arg=10)
    for i in range(num):
        keyboard.press_and_release("pagedown" if page else "down")
        time.sleep(0.05)
    keyboard.release('shift')

def popup_click(popupmenu, name):
    cmd = get_child(popupmenu, name=name, ctrl_type='MenuItem', deep=2)
    win_click(cmd)
    #cmd.click()

def popup_reply(wtop, selects):
    sel = selects.split('#')
    menuname = 'PopupMenu'          # level0
    for s in sel:
        popupmenu  = get_child(wtop, name=menuname, ctrl_type='Menu')
        popup_click(popupmenu, s)
        menuname = s

def butt_is_checked(butt):
    state = butt.legacy_properties()['State']
    return ((state & WIN_BUTT_STATE_CHECKED)!=0)

def win_copy_to_clip(delay = .5):
    keyboard.press_and_release('ctrl+c')
    time.sleep(delay)
    win32clipboard.OpenClipboard()
    new_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return new_data

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
def match_value(pattern, value, usere=False, case_sens=True):
    try:          
        if (not case_sens):
            pattern.lower()     # puo essere regexp
            value.lower()
        if usere:
            return bool(re.match(pattern, str(value)))
        return pattern == value
    except Exception:
        return False
  
def check_control(control, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         usere=False, case_sens=True, visible_only=False):
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
                if not match_value(name, control.window_text(), usere, case_sens):
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

DEEP_ALL = -1

def get_child(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         deep=1, usere=False, case_sens=True, visible_only=False):
    
    if not parent_wnd:
        return None
            
    try:
        elements = parent_wnd.descendants() if deep==DEEP_ALL else parent_wnd.children()
        
        for element in elements:
            if check_control(element, name, ctrl_type, class_name, automation_id, handle, texts,
                              usere, case_sens, visible_only):
                return element
            
        # voglio ricercare top-first, non deep-first
        if (deep!=DEEP_ALL and deep > 1):
            for element in elements:     
                subres = get_child(element, name, ctrl_type, class_name, automation_id, handle, texts,
                                     deep-1, usere, case_sens, visible_only)
                if (subres):
                    return subres
    except Exception:
        pass
        
    return None

def get_child_retry(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         deep=1, usere=False, case_sens=True, visible_only=False,
                         attempt=5, wait_init=0.25,  delay=1, wait_end=0.25):
    time.sleep(wait_init)
    while attempt>0:
        #print (attempt)
        cld = get_child(parent_wnd, name, ctrl_type, class_name, automation_id, handle, texts,
                         deep, usere, case_sens, visible_only)
        if (cld):
            time.sleep(wait_end) 
            return cld
        
        attempt -= 1
        if attempt==0:
            return None
        time.sleep(delay) 
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
#region List - Chrome
######################################################################################################

def list_select(list_control, value, usere=False):
    list_item = get_child(list_control, name=value, usere=usere)
    
    if (not list_item):
        return False
    win_click(list_item, wait_end=0.5)
    print("click")
    return True
def list_select_texts(list_control, text_values, usere=False):
    list_item = get_child(list_control, texts=text_values, usere=usere)

    if (not list_item):
      return False
    win_click(list_item, wait_end=0.5)
    return True

#endregion

######################################################################################################
#region List - Windows 
######################################################################################################

def list_check(list_control, Names="*", value:bool=True, wait_end=0.25):
    items = list_control.children()
    
    for item in items:
        if item.element_info.control_type=='ListItem':
            if (Names=='*' or item.window_text() in Names):
                if item.iface_toggle.CurrentToggleState != int(value):
                    item.iface_toggle.Toggle()
    time.sleep(wait_end)

#endregion

######################################################################################################
# Warning - Confirm 
######################################################################################################
#region
def warning_replay(wtop, mess, butt):
    warning = get_child(wtop, name='Coherence', ctrl_type='Pane')
    if warning:
        message = get_child(warning, ctrl_type='Text', usere=False).window_text()
        assert (mess in message)
        butt = get_child(warning, name=butt, ctrl_type='Button')
        win_click(butt)
        return True
    return False
#endregion

ROBOT_MAX_BUFFER_SIZE   = 4096                              # ?
#WM_ROBOT_GRID_COMMAND = win32con.WM_USER + 199
ROBOT_PORT              = 63888                             # reply
ROBOT_SIGNATURE         = 55555                             # check sender
ROBOT_CMD_BASE          = 22220                             # aske fun
ROBOT_CMD_GET_HEADER    = ROBOT_CMD_BASE + 0

import win32gui
import socket
import ctypes

class RobotCommunicator:
    def __init__(self, window_handle):
        self.window_handle = window_handle
        self.server = None
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server:
            self.server.close()
            
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', ROBOT_PORT))
        self.server.listen(1)
        return self.server
        
    def send_command(self, command_id, input_str, timeout):
        try:
            # Prepare data structure
            class COPYDATASTRUCT(ctypes.Structure):
                _fields_ = [
                    ("dwData", ctypes.wintypes.LPARAM),
                    ("cbData", ctypes.wintypes.DWORD),
                    ("lpData", ctypes.c_void_p)
                ]
            
            # Encode input data
            data = input_str.encode('utf-8') if input_str else b''
            buffer = ctypes.create_string_buffer(data)
            
            # Setup COPYDATA structure
            cds = COPYDATASTRUCT()
            cds.dwData = command_id
            cds.cbData = len(data)
            cds.lpData = ctypes.cast(buffer, ctypes.c_void_p).value
            
            wparam = (ROBOT_SIGNATURE << 16) | ROBOT_PORT
            
            # Start server before sending message
            self.start_server()
            self.server.settimeout(timeout)  # 2 seconds timeout
            
            # Send message
            result = win32gui.SendMessage(
                self.window_handle,
                win32con.WM_COPYDATA,
                wparam,
                ctypes.addressof(cds)
            )
            
            if result == 1:
                return self._receive_response()
            
            return result
            
        except Exception as e:
            print(f"Error in send_command: {e}")
            return None
            
    def _receive_response(self):
        try:
            client_socket, _ = self.server.accept()
            data = client_socket.recv(ROBOT_MAX_BUFFER_SIZE).decode('utf-8')
            client_socket.close()
            return data
        except socket.timeout:
            print("Socket timeout while waiting for response")
            return None
        except Exception as e:
            print(f"Error receiving response: {e}")
            return None

def robot_send(window_handle, command_id, input_str="", timeout = 2):
    with RobotCommunicator(window_handle) as communicator:
        return communicator.send_command(command_id, input_str, timeout=timeout)


#endregion


######################################################################################################
# Warning Reply
######################################################################################################
#region
def warning_replay(wtop, mess, butt):
    warning = get_child(wtop, name='Coherence', ctrl_type='Pane')
    if warning:
        message = get_child(warning, ctrl_type='Text', usere=False).window_text()
        assert (mess in message)
        butt = get_child(warning, name=butt, ctrl_type='Button')
        win_click(butt)
        return True
    return False
#endregion


######################################################################################################
#  Dump - (Develop Helpers)
######################################################################################################
#region

def dump_uia_detail(item):
    properties = item.legacy_properties()
    print('### legacy_properties:')
    print(properties)

    props = item.get_properties()
    print('### get_properties:')
    print(props)

    try:
        wrapper = item.wrapper_object()
        print(wrapper.get_toggle_state())
    except:
        print("Toggle interface non disponibile")

    try:
        print(item.iface_toggle.CurrentToggleState())
    except:
        print("Toggle interface non disponibile")

    print('### dir(item):')
    print(dir(item))  # mostra tutti i metodi/proprietà disponibili


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
        

def dump_uia_detail(item, indent=""):
    """
    Funzione per analizzare e stampare tutti i dettagli disponibili di un elemento UIA
    Args:
        item: Elemento UIA da analizzare
        indent: Indentazione per output annidato (default "")
    """
    def print_section(title, indent=""):
        print(f"\n{indent}{'='*20} {title} {'='*20}")
    
    def safe_get(func, default="Non disponibile"):
        try:
            result = func()
            return result
        except Exception as e:
            return f"{default} (Errore: {str(e)})"
    
    # Informazioni base dell'elemento
    print_section("INFORMAZIONI BASE", indent)
    print(f"{indent}Elemento: {item}")
    print(f"{indent}Tipo: {type(item)}")
    
    # Element Info
    print_section("ELEMENT INFO", indent)
    if hasattr(item, 'element_info'):
        ei = item.element_info
        print(f"{indent}Control Type: {safe_get(lambda: ei.control_type)}")
        print(f"{indent}Class Name: {safe_get(lambda: ei.class_name)}")
        print(f"{indent}Name: {safe_get(lambda: ei.name)}")
        print(f"{indent}Handle: {safe_get(lambda: ei.handle)}")
        print(f"{indent}Runtime ID: {safe_get(lambda: ei.runtime_id)}")
        print(f"{indent}Rectangle: {safe_get(lambda: ei.rectangle)}")
        print(f"{indent}Process ID: {safe_get(lambda: ei.process_id)}")
    
    # Properties
    print_section("PROPERTIES", indent)
    print(f"{indent}Legacy Properties:")
    legacy_props = safe_get(lambda: item.legacy_properties())
    for key, value in legacy_props.items() if isinstance(legacy_props, dict) else []:
        print(f"{indent}  {key}: {value}")
    
    print(f"\n{indent}Get Properties:")
    props = safe_get(lambda: item.get_properties())
    for key, value in props.items() if isinstance(props, dict) else []:
        print(f"{indent}  {key}: {value}")
    
    # Stati e Toggle
    print_section("STATI E TOGGLE", indent)
    print(f"{indent}Toggle State: {safe_get(lambda: item.get_toggle_state())}")
    print(f"{indent}Is Selected: {safe_get(lambda: item.is_selected())}")
    print(f"{indent}Is Enabled: {safe_get(lambda: item.is_enabled())}")
    print(f"{indent}Is Visible: {safe_get(lambda: item.is_visible())}")
    
    # Pattern Interfaces
    print_section("PATTERN INTERFACES", indent)
    patterns = [
        'iface_toggle', 'iface_selection', 'iface_selection_item',
        'iface_value', 'iface_range_value', 'iface_grid', 'iface_table',
        'iface_text', 'iface_invoke', 'iface_expand_collapse'
    ]
    
    # Gestione sicura dei pattern
    for pattern in patterns:
        try:
            interface = getattr(item, pattern, None)
            if interface is not None:
                print(f"{indent}{pattern}: Disponibile")
                # Gestione sicura dei metodi specifici per pattern
                if pattern == 'iface_toggle':
                    print(f"{indent}  Toggle State: {safe_get(lambda: interface.CurrentToggleState())}")
                elif pattern == 'iface_value':
                    print(f"{indent}  Value: {safe_get(lambda: interface.CurrentValue())}")
        except Exception as e:
            print(f"{indent}{pattern}: Non disponibile (Errore: {str(e)})")
    
    # Metodi disponibili
    print_section("METODI DISPONIBILI", indent)
    methods = [method for method in dir(item) if not method.startswith('_')]
    print(f"{indent}Metodi totali: {len(methods)}")
    for method in sorted(methods):
        print(f"{indent}  {method}")

#endregion