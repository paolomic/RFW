import keyboard
import mouse
import time

# Import Path - Assudo
import sys
from pathlib import Path

#strpath = r'C:\work\disks\D\prog\RFW\utils'
#sys.path.append(strpath) 

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl
from utl_app import env
from utl_win import sleep, VERIFY, RAISE, ROBOT_RES
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud

#TODO Spostare in tests/modules (problema include)


######################################################
###  Session Parameter
#region 

COH_PATH =              r'C:\work\disks\D\COH_x64\bin\Coherence.exe'                # TODO: JSon File ?
COH_ADDIN=              ['MetaMarket','UserPages']

COH_WSP=                r"C:\work\disks\D\wsp_c\robot_test.wsp4"
COH_PRIMARY=            '192.168.200.127'         
COH_PORT=               '28000'         
COH_USER=               'MARI'         
COH_PASS=               '*'         
COH_BAND_SAVE=           True

COH_EXC=                'BIT'
COH_MRK=                'MTA'
COH_SEC=                'AUTOGRILL SPA'
COH_PRICE =             '95.01'
COH_QTY =               '100'
COH_ALIAS =             'KATIA'
COH_CLIENTID =          'MARI'
COH_CLIENTACC =         'TEST'

COH_SAVE_WSP_ONCLOSE =  'Yes'

if (1):                 # FTX
    COH_PRIMARY=        '10.91.204.22'         
    COH_PORT=           '42900'         
    COH_USER=           '99999@99999'         
    COH_PASS=           '*'         
    COH_EXC=            'HIMTF'
    COH_MRK=            'MTF'
    COH_SEC=            'BTP 1 ST 46 3,25%'

#endregion


######################################################
### Robot Operations
#region 
def do_new_session(arg):
    path_wsp = Path(COH_WSP)
    if (path_wsp.exists()):
        path_wsp.unlink()
    VERIFY(not path_wsp.exists(), 'Wsp Exist')
    #path_wsp_folder = Path(COH_WSP.replace('.wsp4', '.wsp4_wrk'))
    #if (path_wsp_folder.exists()):
    #    path_wsp_folder.rmdir()
    #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

def do_start_dialog(arg):
    edit = uw.get_child_chk(env.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_WSP)

    list = uw.get_child_chk(env.wtop, name='Import From', ctrl_type='List', deep=3)
    uw.list_check(list, '*', False)
    uw.list_check(list, arg, True)

    butt = uw.get_child_chk(env.wtop, automation_id='1', ctrl_type='Button', deep=3)
    is_create = butt.window_text()=='Create'
    VERIFY(is_create, 'Can`t Create New Workspace')

    uw.win_click(butt, wait_end=0.5)
    uw.warning_replay(env.wtop, 'This workspace has not been closed properly', 'No')

    sleep(3.5)                                                                         # todo : Smart Wait                     
    env.reload()  
        
def do_setting_init(arg):
    pane = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Pane', deep=3)
    list = uw.get_child_chk(pane, automation_id='103', ctrl_type='List', deep=3)

    ### Connection
    edit = uw.get_child_chk(pane, name='Primary', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_PRIMARY)
    edit = uw.get_child_chk(pane, name='Port', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_PORT)
    edit = uw.get_child_chk(pane, name='User name', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_USER)
    edit = uw.get_child_chk(pane, automation_id='11303', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_PASS)
    
    if COH_BAND_SAVE:
        butt = uw.get_child_chk(pane, name='Bandwidth Saving', ctrl_type='CheckBox', deep=3)
        if not uw.butt_is_checked(butt):
            uw.win_click(butt)

    ### MetaMarket
    uw.list_select(list, "MetaMarket")

    trace = uw.get_child_chk(pane, name='Trace Level', ctrl_type='Custom', deep=3)
    uw.win_click(trace, mode='combo')

    #sleep(.25)
    #ud.dump_uia_tree(env.wtop)         # non c'e' lista popup

    uw.hide_select(-1)                  # Todo Control Inside
    keyboard.press("enter")             # Confirm Selection
    sleep(.25)

    ### WorkSpace
    uw.list_select(list, "Workspace")

    combo = uw.get_child_chk(pane, automation_id='11347', ctrl_type='ComboBox', deep=3) # Todo: Input Per Valore
    uw.win_click(combo)
    keyboard.press("end")
    keyboard.press("enter")

    combo = uw.get_child_chk(pane, automation_id='11345', ctrl_type='ComboBox', deep=3)
    uw.win_click(combo)
    keyboard.press("end")
    keyboard.press("enter")

    ### OK
    butt = uw.get_child_chk(pane, name='OK', ctrl_type='Button', deep=3)
    uw.win_click(butt)

def do_start_connections(arg):
    addins = ['MetaMarket']                                                     # TODO pass form Robot ?
    for addin in addins:
        butt = env.select_ribbon_butt(addin, 'Auto Connect')
        if not uw.butt_is_checked(butt):
            uw.win_click(butt)

    butt = env.select_ribbon_butt('Home', 'Auto Connect')
    if not uw.butt_is_checked(butt):
        uw.win_click(butt)

    if uw.statusbar_wait(env.st_bar, 'Ready', attempt=15, delay=2):             # Wait for Connection Ready
        print ('Connection Ready')
    else:
        RAISE("Connection Fail")

def do_search_security(arg):
    # la pg viene generata sotto main-node coherence
    env.click_ribbon_butt('Trading', 'Security Browser')
    page = uw.get_child_chk(env.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    grid = uw.get_child_chk(page, name='StingrayGrid', deep=9)

    uw.win_resize(page, 888, 444)

    search_edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
    search_butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
    #uw.edit_set(edit, '')
    #uw.win_click(butt, wait_end=.5)

    treekey = f'{COH_EXC} - {COH_MRK}'
    item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
    uw.win_click(item)

    uw.edit_set(search_edit, COH_SEC)
    uw.win_click(search_butt)

    status_num = uw.get_child_chk(page, name='No. of Rows: .*', ctrl_type='Text', deep=10, use_re=True)
    print(f'status_num {status_num}')
    VERIFY(status_num.window_text()=='No. of Rows: 1', 'Not Such Unique Security')           # Todo : Fare Meglio il Test

    grid = status_num = uw.get_child_chk(page, automation_id='59661', ctrl_type='Pane', deep=10, use_re=True)
    # hide
    uw.win_click(grid, mode='grid_row1')
    mouse.click('right')
    sleep(0.25)

    uw.popup_reply(env.wtop, 'New#Care Order')          # Il popup viene generato sotto level top - anche il sotto menu
    uw.page_close(page, save_as='security_search')

def do_new_care_order(arg):
    dlg = uw.get_child_chk(env.wtop, name="New Care Order.*", ctrl_type="Pane", use_re=1)
    adv = uw.get_child_chk(dlg, automation_id='13652', ctrl_type="CheckBox", use_re=1)
    if not uw.butt_is_checked(adv):
        uw.win_click(adv)
    dlgadv = uw.get_child_chk(dlg, name="Order Advanced Parameters", ctrl_type="Pane")

    edit = uw.get_child_chk(dlg, automation_id='12216')     # Q
    uw.edit_set(edit, COH_QTY)

    edit = uw.get_child_chk(dlg, automation_id='12214')     # P
    uw.edit_set(edit, COH_PRICE)
    
    edit = uw.get_child_chk(dlg, automation_id='12796')     # Alias
    uw.win_click(edit)
    keyboard.write(COH_ALIAS)                               # popup is hide - or edit_set
    keyboard.press("tab")
        
    start_time = utl.get_now_sec()                           # Note
    mytag = f'pwa_{start_time.replace(":","_")}' 
    edit = uw.get_child_chk(dlgadv, automation_id='12954')  
    uw.edit_set(edit, mytag)

    uw.win_close(dlgadv)

    but = uw.get_child_chk(dlg, automation_id='1')          # Buy     
    uw.win_click(but)

    log_path = uw.get_log_path(COH_WSP, 'MetaMarket')
    order = ul.GetLogRows(log_path, 'CLIENT_ORDER', 'ComplianceText', mytag, start_time, retry = 4, wait_s = 1)

    if (not order):
        RAISE("Order not Found")

    uw.win_close(dlg)
    
    return order['fields']['OrderID']

def do_select_order(arg):
    order_id = arg
    env.click_ribbon_butt('Trading', 'Orders')
    page = uw.get_child_chk(env.wtop, name='Orders.*', ctrl_type='Pane', use_re=1, deep=2)
    
    edit = uw.get_child_chk(page, name='Order ID', ctrl_type='Edit', deep=5)  
    uw.edit_set(edit, order_id)

    butt = uw.get_child_chk(page, name='Apply', ctrl_type='Button', deep=5)  
    uw.win_click(butt)

    status_num = uw.get_child_chk(page, name='No. of Rows: .*', ctrl_type='Text', deep=10, use_re=True)
    print(f'status_num {status_num}')
    VERIFY(status_num==1, 'Insert Orfed FIlter Failure')

    uw.page_save(page, 'order_filtered', time_tag=True)

def do_grid_sample(arg):                         
    env.click_ribbon_butt('Trading', 'Security Browser')                            # todo: Gia una aperta : selezionare l utima ?
    page = uw.get_child_chk(env.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    grid = uw.get_child_chk(page, name='StingrayGrid', deep=9)

    uw.win_resize(page, 999, 444)

    #search_edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
    #search_butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
    #uw.edit_set(edit, '')
    #uw.win_click(butt, wait_end=.5)

    treekey = f'{COH_EXC} - {COH_MRK}'
    item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
    uw.win_click(item)

    # Esempio Get sheet info
    ug.set_show_all_2(env.wtop, grid)
    grid_mng = ug.create_by_win(grid)
    
    # esempio scroll
    ug.scroll_home(grid_mng)

    # esempio sort
    ug.set_sort(grid_mng,'default')
    ug.set_sort(grid_mng, [['Section','DESC'],['Security Ref.','ASC']])

    #esempio Import Rows
    ug.import_rows(grid_mng, 10, mode='pg')
    
    # esempio Data Search-Use
    print (f'Collected Rows: {grid_mng.get_row_num()}')
    sel = grid_mng.search_first_match({"Security Ref.": COH_SEC})      # piu segmenti con , 
    print(f'Find {1 if sel else 0} Row')
    VERIFY(sel, 'Security not Found')
    #print(f'Find Row: {sel}')
    print(f'Security Status {sel["Status"]}')
    uw.page_save(page, 'security_grid_demo', time_tag=True)

def do_close_session(arg):                         
    pass

#endregion


######################################################
# Generic Caller
def robot_run(fun_name:str, arg:str='', session='hang'):
    def manage_session(session):
        if session=='new':
            env.launch_app(COH_PATH)
        else:
            env.hang_app(COH_PATH)
        if session=='kill':
            uw.session_close(env.wtop, wait_init=1, wait_end=1, save_wsp=COH_SAVE_WSP_ONCLOSE)
    def verify_session(session):
        if session=='kill':
            exist = 0
            try:
                env.hang_app(COH_PATH)
                exist=1
            except Exception as e:
                pass
            VERIFY(not exist, 'Close Session Failed. Process still Exists')
        else:
            VERIFY(env.app and env.wtop, "Hang or New Session Failed")
    try:
        manage_session(session)
        verify_session(session)
        func = globals().get(fun_name)
        result = func(arg)
        return ROBOT_RES('ok', result)
    except Exception as e:
        return ROBOT_RES('no', str(e)) 
    
    
######################################################
# Main DEBUG 

def prova(arg):
    env.hang_app(COH_PATH)
    page = uw.get_child_chk(env.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    #uw.win_move(page, 12, 12)
    uw.win_resize(page, 444, 444)
    
if __name__ == '__main__':
    select = 1
    if (select==1):
        print(robot_run('do_close_session', session='kill') )


