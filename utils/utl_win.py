import keyboard
import mouse

from pywinauto import Desktop

from datetime import datetime
import time
import re
import win32clipboard

from win32gui import FindWindow, PostMessage, GetCursorInfo
import win32.lib.win32con as win32con

WIN_BUTT_STATE_CHECKED          = (1<<4)

##########################################################
# Generic
##########################################################
#region
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

def all_substr_in(subs:list, thestr:str, use_case=True):        
    if not is_array(subs):
        if (not use_case):
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

def edit_set(edit, value, wait_end=0.2):
    edit.iface_value.SetValue(value)
    time.sleep(wait_end)

def get_today_iso():
  return datetime.now().strftime('%Y%m%d')

def get_log_path(wsp_path, logname):
  filename = f'{logname}_{get_today_iso()}.log'
  return f'{wsp_path}_wrk\\Logs\\{filename}'

def wait_cursor_normal(wait_init=0.1, wait_in=0.5, wait_end=0.2, timeout=15):
    time.sleep(wait_init)
    start = datetime.now()
    while (1):
        cursor_info = GetCursorInfo()
        handle = cursor_info[1]
        #print(f'handle {handle}')       # Debug
        if (handle!=65545):
            break
        if (datetime.now()-start).seconds > timeout :
            break
        time.sleep(wait_in)     # retry

    time.sleep(wait_end)

def end_session():
    print ('## Session End ##')
    exit()
#endregion

##########################################################
# Windows
##########################################################
#region
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
        return(x,y)   # absolute                                           # abs cord

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
    return (click_x, click_y)       

def win_mouse_move(window, client_x, client_y, wait_end=0.25, arg=None): 
    rect = window.element_info.rectangle
    abs_x = rect.left+client_x
    abs_y = rect.top+client_y
    mouse.move(abs_x,abs_y)

def win_get_top(win):
    go = 1
    while (go):
        p = win.parent()
        if not p or win.element_info.control_type == "Window":
            break
        win = p
    
    return win

#endregion

##########################################################
# PopUp - Warning
##########################################################
#region
def popup_click(popupmenu, name, skip_disabled=False):
    cmd = get_child(popupmenu, name=name, ctrl_type='MenuItem', deep=2, enable_only=False)
    if (skip_disabled and not cmd.is_enabled()):
        keyboard.press_and_release('esc')
        return -1
    win_click(cmd)
    #cmd.click()
    return 1

def popup_reply(wtop, selects, wait_init=0.2, wait_end=0.2, skip_disabled=False):
    time.sleep(wait_init)
    sel = selects.split('#')
    menuname = 'PopupMenu'          # level0
    for s in sel:
        popupmenu  = get_child(wtop, name=menuname, ctrl_type='Menu', enable_only=False)
        if (skip_disabled and not popupmenu.is_enabled()):
            keyboard.press_and_release('esc')
            return -1
        popup_click(popupmenu, s, skip_disabled=skip_disabled)
        menuname = s
    time.sleep(wait_end)
    return 1

def warning_replay(wtop, mess, butt):
    warning = get_child(wtop, name='Coherence', ctrl_type='Pane')
    if warning:
        message = get_child(warning, ctrl_type='Text', use_re=False).window_text()
        assert (mess in message)
        butt = get_child(warning, name=butt, ctrl_type='Button')
        win_click(butt)
        return True
    return False

#endregion

##########################################################
# Grid
##########################################################
#region
def grid_select_all(grid):
    win_click(grid, mode='grid_col1')
    win_click(grid, mode='grid_tl')

def grid_select_rows(grid, num, mode="row", home=True):
    if num==0:
        return grid_select_all(grid)
    if(home):
        win_click(grid)
        keyboard.press_and_release('ctrl+home')
    win_click(grid, mode='grid_row', arg=1)
    keyboard.press('shift')
    #win_click(grid, mode='grid_row', arg=10)
    for i in range(num):
        keyboard.press_and_release("pagedown" if mode=="page" else "down")
        time.sleep(0.05)
    keyboard.release('shift')

def win_copy_to_clip(wait_init = .5):
    keyboard.press_and_release('ctrl+c')
    wait_cursor_normal(wait_init=wait_init)
    win32clipboard.OpenClipboard()
    new_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return new_data

#endregion

##########################################################
# find_window
##########################################################
#region
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
#endregion

##########################################################
# get_child
##########################################################
#region
def match_value(pattern, value, use_re=False, use_case=True):
    try:          
        if (not use_case):
            pattern.lower()     # puo essere regexp
            value.lower()
        if use_re:
            return bool(re.match(pattern, str(value)))
        return pattern == value
    except Exception:
        return False
  
def check_control(control, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         use_re=False, use_case=True, visible_only=False, enable_only=True):
    try:
        if enable_only:
            try:
                if not control.is_enabled():
                    return False
            except Exception:
                pass
        
        if visible_only:
            try:
                if not control.is_visible():
                    return False
            except Exception:
                pass
            
        if name is not None:
            try:
                if not match_value(name, control.window_text(), use_re, use_case):
                    return False
            except Exception:
                return False

        if ctrl_type is not None:
            try:
                if not match_value(ctrl_type, control.element_info.control_type, False, use_case):
                    return False
            except Exception:
                return False
        
        if class_name is not None:
            try:
                if not match_value(class_name, control.element_info.class_name, False, use_case):
                    return False
            except Exception:
                return False


        if automation_id is not None:
            try:
                if not match_value(automation_id, control.element_info.automation_id, False, use_case):
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

                if not all_substr_in(texts, array_to_str(prop_texts), use_case):
                    return False
            except Exception:
                return False      
        
        return True
            
    except Exception:
        return False

DEEP_ALL = -1

def get_child(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         deep=1, use_re=False, use_case=True, visible_only=False, enable_only=True):
    
    if not parent_wnd:
        return None
            
    try:
        elements = parent_wnd.descendants() if deep==DEEP_ALL else parent_wnd.children()
        
        for element in elements:
            if check_control(element, name, ctrl_type, class_name, automation_id, handle, texts,
                              use_re, use_case, visible_only, enable_only):
                return element
            
        # voglio ricercare top-first, non deep-first
        if (deep!=DEEP_ALL and deep > 1):
            for element in elements:     
                subres = get_child(element, name, ctrl_type, class_name, automation_id, handle, texts,
                                     deep-1, use_re, use_case, visible_only, enable_only)
                if (subres):
                    return subres
    except Exception:
        pass
        
    return None

def get_child_retry(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         deep=1, use_re=False, use_case=True, visible_only=False, enable_only=True,
                         attempt=5, wait_init=0.25,  delay=1, wait_end=0.25):
    time.sleep(wait_init)
    while attempt>0:
        #print (attempt)
        cld = get_child(parent_wnd, name, ctrl_type, class_name, automation_id, handle, texts,
                         deep, use_re, use_case, visible_only, enable_only)
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


#endregion

##########################################################
#List - Chrome
##########################################################
#region
def list_select(list_control, value, use_re=False):
    list_item = get_child(list_control, name=value, use_re=use_re)
    
    if (not list_item):
        return False
    win_click(list_item, wait_end=0.5)
    print("click")
    return True

def list_select_texts(list_control, text_values, use_re=False):
    list_item = get_child(list_control, texts=text_values, use_re=use_re)

    if (not list_item):
      return False
    win_click(list_item, wait_end=0.5)
    return True

#endregion

##########################################################
# List - Windows 
##########################################################
#region
def list_check(list_control, Names="*", value:bool=True, wait_end=0.25):
    items = list_control.children()
    
    for item in items:
        if item.element_info.control_type=='ListItem':
            if (Names=='*' or item.window_text() in Names):
                if item.iface_toggle.CurrentToggleState != int(value):
                    item.iface_toggle.Toggle()
    time.sleep(wait_end)

def butt_is_checked(butt):
    state = butt.legacy_properties()['State']
    return ((state & WIN_BUTT_STATE_CHECKED)!=0)

#endregion

