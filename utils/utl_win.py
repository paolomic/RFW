import keyboard
import mouse
import os
import signal

from pywinauto import Desktop, Application, findwindows
from pathlib import Path

from datetime import datetime
import time
import re
import win32clipboard

import win32gui
from win32gui import FindWindow, PostMessage, GetCursorInfo

import win32.lib.win32con as win32con
import utl  as utl
import utl_app as ua
from utl_config import config
import utl_dump as ud


WIN_BUTT_STATE_CHECKED          = (1<<4)

##########################################################
# Generic
##########################################################
#region

def sleep(sec):
    opt_speed = config.get('opt.speed')
    if opt_speed:
        speed = float(opt_speed)/100  
    else:
        speed=1
    
    time.sleep(sec/speed)


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
    

def edit_set(edit, value, wait_end=0.3):
    edit.iface_value.SetValue(value)
    sleep(wait_end)

def edit_set_manual(edit, value, reset=False, wait_end=0.3):
    win_click(edit)
    if reset:
        keyboard.press_and_release('ctrl+a')
        keyboard.press_and_release('del')
    keyboard.write(value)
    sleep(wait_end)

def get_today_iso():
  return datetime.now().strftime('%Y%m%d')

def get_log_path(wsp_path, logname):
  filename = f'{logname}_{get_today_iso()}.log'
  return f'{wsp_path}_wrk\\Logs\\{filename}'

def wait_cursor_normal(wait_init=0.1, wait_in=0.5, wait_end=0.2, timeout=15):
    sleep(wait_init)
    start = datetime.now()
    while (1):
        cursor_info = GetCursorInfo()
        handle = cursor_info[1]
        #print(f'handle {handle}')       # Debug
        if (handle!=65545):
            break
        if (datetime.now()-start).seconds > timeout :
            break
        sleep(wait_in)     # retry

    sleep(wait_end)

#endregion

##########################################################
# Robot
##########################################################

def ROBOT_RES(status='ok', info=''):
    sleep(0.3)
    if (info==None):
        info=""
    return {
        "status": status,
        'info': info}


##########################################################
# Sessione and Pages
##########################################################

def workspace_remove(wsp_path):
    path_wsp = Path(wsp_path)
    if (path_wsp.exists()):
        path_wsp.unlink()
    ua.VERIFY(not path_wsp.exists(), 'Wsp Exist')
    #path_wsp_folder = Path(COH_WSP.replace('.wsp4', '.wsp4_wrk'))
    #if (path_wsp_folder.exists()):
    #    path_wsp_folder.rmdir()
    #ua.VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

def session_logon():
    butt = ua.app.select_ribbon_butt('Home', 'Auto Connect')
    if not butt_is_checked(butt):
        win_click(butt)

def session_logoff():
    butt = ua.app.select_ribbon_butt('Home', 'Auto Connect')
    if butt_is_checked(butt):
        win_click(butt)
        warning_replay('Do you want to disable Auto Connect mode and stop all connections?', 'OK')

def session_close (wtop, wait_init=.5, wait_end=.5, logoff=False, save_wsp=False):
    sleep(wait_init)
    if (logoff):
        session_logoff()
    if config.get('opt.close_all_pages')=='yes':
        page_close_all()
    save_wsp=config.get('opt.save_wsp_onclose')=='yes'
    win_close(wtop, wait_end=0.3)
    warning_replay('Do you want to close current workspace', 'OK')
    warning_replay('Do you want to save current workspace?', 'Yes' if save_wsp else 'No')
    sleep(wait_end)

def page_save(page, name, time_tag=False):
    if not name:
        return

    page.set_focus()
    keyboard.press_and_release('ctrl+s')
    sleep(0.2)
    # non e' chiaro dove e' collocata. se prima ho aperto newdialog ad esempio

    popup = get_child_chk(page.parent(), name='Save page', ctrl_type='Pane', deep=3, verify=False)  
    if popup:
        if name:
            if time_tag:
                now = utl.get_now_sec()                            # Note
                name = name + '_' + now.replace(":","_")
            edit = get_child_chk(popup, ctrl_type='Edit')
            edit_set(edit, name)
        butt = get_child_chk(popup, name='OK', ctrl_type='Button')
        win_click(butt)
        sleep(0.2)
        warning_replay('Do you want to replace the page saved with this name.*', butt='OK', use_re=True)

        #warning = get_child_chk(popup, name='Coherence', ctrl_type='Pane', verify=False)
        #if warning:
        #    message = get_child_chk(warning, name='Do you want to replace the page saved with this name.*', ctrl_type='Text', use_re=True, verify=False)
        #    if (message):
        #        butt = get_child_chk(warning, name='OK', ctrl_type='Button')
        #        win_click(butt)


def page_close(page, save_as=None, time_tag=False):
    if save_as:
        page_save(page, save_as, time_tag=time_tag)
    win_close(page)
    warning_replay('Do you want to save the page.*before closing.*', 'No', use_re=True)

def page_close_all(save_as=None, time_tag=False):
    elements = ua.app.wtop.children() 
    for elem in elements:
        if (page_get_grid(elem, verify=False)):
            page_close(elem, save_as=save_as, time_tag=time_tag)

def page_get_num(page):
    pattern = 'No\. *of ([a-zA-Z0-9_]*): *([0-9])'
    text = get_child_chk(page, name=pattern, ctrl_type='Text', deep=10, use_re=True)
    if (text):
        return int (re.match(pattern, text.window_text())[2])
    return None

def page_get_grid(page, verify=True):
    grid = get_child_chk(page, name='StingrayGrid', deep=9, verify=verify)
    return grid



##########################################################
# Move Resize
##########################################################

#page.set_focus()       # todo per Order Dlg non lo mette in fronte

def win_move(window, x, y):
  rect = window.element_info.rectangle
  win32gui.MoveWindow(window.handle, x, y, rect.width(), rect.height(), True)

def win_resize(window, w, h):
  #window.iface_transform.Resize(w, h)
  rect = window.element_info.rectangle
  win32gui.MoveWindow(window.handle, rect.left, rect.top, w, h, True)

def win_maximize(window, maximize=True):
    is_maximized = window.is_maximized()
    if maximize and not is_maximized:
        window.maximize()
    elif not maximize and is_maximized:
        window.restore()

##########################################################
# Windows
##########################################################
#region
def win_close(win, wait_end=0.25):
    PostMessage(win.handle, win32con.WM_CLOSE, 0, 0)
    sleep(wait_end)

def win_activate(window, unminimize = True, wait_end=0.25, wait_restore=0.5):
    window.set_focus()
   
    if unminimize and window.element_info.control_type == 'Window' and window.is_minimized():
        window.restore()
        sleep(wait_restore)  # Attende il ripristino
    sleep(wait_end)

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

    if (mode=='grid_header'):
        click_x = (rect.left +30)
        click_y = (rect.top + 6) 

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
    sleep(wait_end)
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
    cmd = get_child_chk(popupmenu, name=name, ctrl_type='MenuItem', deep=2, enable_only=False)
    if (skip_disabled and not cmd.is_enabled()):
        keyboard.press_and_release('esc')
        return -1
    win_click(cmd)
    #cmd.click()
    return 1

def popup_reply(wtop, selects, wait_init=0.2, wait_end=0.2, skip_disabled=False):
    sleep(wait_init)
    sel = selects.split('#')
    menuname = 'PopupMenu'          # level0
    for s in sel:
        popupmenu  = get_child_chk(wtop, name=menuname, ctrl_type='Menu', enable_only=False)
        if (skip_disabled and not popupmenu.is_enabled()):
            keyboard.press_and_release('esc')
            return -1
        popup_click(popupmenu, s, skip_disabled=skip_disabled)
        menuname = s
    sleep(wait_end)
    return 1

def warning_replay(mess, butt, root=None, title='Coherence', use_re=False, deep=3):
    if not root:
        root=ua.app.wtop
    popup = get_child_chk(root, name=title, ctrl_type='Pane', verify=False, deep=deep)
    if popup:
        message = get_child_chk(popup, ctrl_type='Text', use_re=use_re).window_text()
        message = message.replace('\n', ' ')
        if (use_re and re.match(mess, message)) or (not use_re and (mess in message)):
            butt = get_child_chk(popup, name=butt, ctrl_type='Button')
            win_click(butt)
        else:
            #e' un altro warning - situazione complessa - warning_replay_2
            ua.VERIFY(None, 'Unespected Warning')
        return True
    return False

def warning_replay_2(mess, butt, root=None, title='Coherence', use_re=False, deep=3):
    #works by message - totest
    if not root:
        root=ua.app.wtop
    txt = get_child_chk(root, mess, ctrl_type='Text', use_re=use_re, verify=False, deep=deep)
    if txt:
        popup = txt.parent()
        if popup:
            butt = get_child_chk(popup, name=butt, ctrl_type='Button')
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
        keyboard.press_and_release("pagedown" if mode=="page" or mode=='pg' else "down")
        sleep(0.05)
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

def get_child_chk(parent_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                         deep=1, use_re=False, use_case=True, visible_only=False, enable_only=True, verify=True):
    cld = get_child(parent_wnd, name, ctrl_type, class_name, automation_id, handle, texts,
                         deep, use_re, use_case, visible_only, enable_only)
    
    if(verify and not cld):
        ua.RAISE(f'Item Not Found: Name:{name} Ctrl:{ctrl_type} Class:{class_name} AutId:{automation_id} ')
    
    return cld

def get_child_retry(parent_wnd, name=None, ctrl_type=None, class_name=  None, automation_id=None, handle=None, texts=None,
                         deep=1, use_re=False, use_case=True, visible_only=False, enable_only=True,
                         timeout=2, wait_init=0.25,  delay=1, wait_end=0.25):
    
    to = utl.TimeOut(timeout)
    sleep(wait_init)
    while not to.expired():
        #print (attempt)
        cld = get_child(parent_wnd, name, ctrl_type, class_name, automation_id, handle, texts,
                         deep, use_re, use_case, visible_only, enable_only)
        if (cld):
            sleep(wait_end) 
            return cld
    
        sleep(delay) 
    return None

# patch per trovare se non ho elementi - web Quantity
def get_child_after(child_wnd, name=None, ctrl_type=None, class_name=None, automation_id=None, handle=None, texts=None,
                   use_re=False, use_case=True, visible_only=False, enable_only=True, check=True):
    parent_wnd = child_wnd.parent()
    children = parent_wnd.children()
    found_child = False
    for sibling in children:
        if found_child:
            if check_control(sibling, name, ctrl_type, class_name, automation_id, handle, texts,
                            use_re, use_case, visible_only, enable_only):
                return sibling
        if sibling == child_wnd:
            found_child = True

    if check:
        ua.RAISE(f'Item Not Found After: Name:{name} Ctrl:{ctrl_type} Class:{class_name} AutId:{automation_id} ')
    return None

#TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST 
def win_reload_bytype(item):
    #name = item.window_text()
    #classname = item.element_info.class_name
    ctrltype = item.element_info.control_type

    if ctrltype=='':
        ctrltype=None

    return get_child_chk(item.parent(), ctrl_type=ctrltype)


#endregion

##########################################################
#List - Chrome
##########################################################
#region
def list_select(list_control, value, use_re=False):
    list_item = get_child_chk(list_control, name=value, use_re=use_re)
    
    if (not list_item):
        return False
    win_click(list_item, wait_end=0.5)
    #print("click")
    return True

def list_select_texts(list_control, text_values, use_re=False):
    list_item = get_child_chk(list_control, texts=text_values, use_re=use_re)

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
    sleep(wait_end)

def butt_is_checked(butt):
    state = butt.legacy_properties()['State']
    return ((state & WIN_BUTT_STATE_CHECKED)!=0)

##########################################################
# Get Main Window 
##########################################################
#region

# normal speed
def get_main_wnd(name=None, handle=None, pid=None, use_re=False):
    # riscritta con deepseek + efficente by name
    # todo aggiungere timeout?
    try:
        if handle is not None:
            app = Application(backend='uia').connect(handle=handle)
            return app.window(handle=handle)
        elif pid is not None:
            app = Application(backend='uia').connect(process=pid)
            return app.window()
        elif name is not None:
            if use_re:
                windows = findwindows.find_windows(title_re=name)
            else:
                windows = findwindows.find_windows(title=name)              # tornano Vettori
            if windows:
                handle = windows[0]                                         # prende la 1a
                app = Application(backend='uia').connect(handle=handle)
                return app.window(handle=handle)
        return None
    except Exception as e:
        print(f"Error in get_main_wnd: {e}")
        return None


#  super_fast version
from typing import Optional, Union
from ctypes import windll, create_unicode_buffer, sizeof, byref
import ctypes
import win32process

def get_main_wnd_fast(name: Optional[str] = None, 
                      handle: Optional[int] = None, 
                      pid: Optional[int] = None, 
                      use_re: bool = False) -> Optional[int]:
    """
    Versione ottimizzata che usa direttamente Win32 API.
    Ritorna l'handle della finestra invece dell'oggetto Application.
    """
    try:
        # Se abbiamo già l'handle, verifichiamo solo che la finestra esista
        if handle is not None:
            if win32gui.IsWindow(handle):
                return handle
            return None

        # Se abbiamo il PID, cerchiamo la finestra principale per quel processo
        if pid is not None:
            def callback(hwnd, target_pid):
                try:
                    _, found_pid = win32gui.GetWindowThreadProcessId(hwnd)
                    if found_pid == target_pid and win32gui.IsWindowVisible(hwnd):
                        target_pid[0] = hwnd
                        return False
                except:
                    pass
                return True
            
            result = [None]
            win32gui.EnumWindows(callback, result)
            return result[0]

        # Ricerca per nome - versione ottimizzata
        if name is not None:
            if use_re:
                pattern = re.compile(name)
                def callback(hwnd, results):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if pattern.search(title):
                            results.append(hwnd)
                            return False
                    return True
                
                results = []
                win32gui.EnumWindows(callback, results)
                return results[0] if results else None
            else:
                # Versione più veloce per match esatto
                def callback(hwnd, target_name):
                    if win32gui.IsWindowVisible(hwnd):
                        if win32gui.GetWindowText(hwnd) == target_name:
                            target_name[0] = hwnd
                            return False
                    return True
                
                result = [None]
                win32gui.EnumWindows(callback, result)
                return result[0]

        return None

    except Exception as e:
        print(f"Error in get_main_wnd_fast: {str(e)}")
        return None

# detail by handle
def get_window_info(hwnd: int) -> dict:
    """
    Ottiene informazioni aggiuntive sulla finestra.
    """
    info = {}
    info['title'] = win32gui.GetWindowText(hwnd)
    info['class'] = win32gui.GetClassName(hwnd)
    info['rect'] = win32gui.GetWindowRect(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Corretto qui
    info['pid'] = pid
    return info


#endregion

