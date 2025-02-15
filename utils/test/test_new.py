import keyboard
import mouse
import time

#TODO Spostare questo py in tests/modules (problema include)



#strpath = r'C:\work\disks\D\prog\RFW\utils'
#sys.path.append(strpath) 

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl
from utl_app import app, opt
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud


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

if ( 1 ):                 # FTX
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
    if (path_wsp.exists() and not config.get('opt.reuse_wsp')=='yes'):
        print('Remove Workspace...')
        path_wsp.unlink()
        VERIFY(not path_wsp.exists(), 'Wsp Exist')
    #path_wsp_folder = Path(COH_WSP.replace('.wsp4', '.wsp4_wrk'))
    #if (path_wsp_folder.exists()):
    #    path_wsp_folder.rmdir()
    #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

def do_start_dialog(arg):
    edit = uw.get_child_chk(app.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_WSP)

    list = uw.get_child_chk(app.wtop, name='Import From', ctrl_type='List', deep=3)
    uw.list_check(list, '*', False)
    uw.list_check(list, arg, True)

    butt = uw.get_child_chk(app.wtop, automation_id='1', ctrl_type='Button', deep=3)
    if not config.get('opt.reuse_wsp')=='yes':
        VERIFY(butt.window_text()=='Create', 'Can`t Create New Workspace')

    uw.win_click(butt, wait_end=0.5)
    uw.warning_replay('This workspace has not been closed properly', 'No')
                                                                                   
    app.reload()                                                                            # Smart Wait for new Main Frame   
        
def do_setting_init(arg):
    butt = uw.get_child_chk(app.wtop, name='Settings', ctrl_type='Button', deep=4)          # Settings gia aperto se New Wsp
    uw.win_click(butt)

    pane = uw.get_child_chk(app.wtop, name='Settings', ctrl_type='Pane', deep=3)
    list = uw.get_child_chk(pane, automation_id='103', ctrl_type='List', deep=3)

    ### Connection  - Disable se connection Ready
    try:
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
    except:
        print('Connection is Started')

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

    combo = uw.get_child_chk(pane, automation_id='11347', ctrl_type='ComboBox', deep=3)         # Todo: Input Per Valore
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
    if config.get('opt.close_all_pages')=='yes':
        uw.page_close_all()
    
    addins = ['MetaMarket']                                                     # TODO pass form Robot ?
    for addin in addins:
        butt = app.select_ribbon_butt(addin, 'Auto Connect')
        if not uw.butt_is_checked(butt):
            uw.win_click(butt)

    butt = app.select_ribbon_butt('Home', 'Auto Connect')
    if not uw.butt_is_checked(butt):
        uw.win_click(butt)

    if app.wait_conn_ready(to_sec=120, to_err_sec=5, delay=2):
        print ('Connection Ready')
    else:
        RAISE("Connection Fail")

def do_search_security(arg):
    # la pg viene generata sotto main-node coherence
    app.click_ribbon_butt('Trading', 'Security Browser')
    page = uw.get_child_chk(app.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    grid = uw.page_get_grid(page)

    uw.win_resize(page, 1400, 450)

    search_edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
    search_butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
    #uw.edit_set(edit, '')
    #uw.win_click(butt, wait_end=.5)

    treekey = f'{COH_EXC} - {COH_MRK}'
    item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
    uw.win_click(item)

    uw.edit_set(search_edit, COH_SEC)
    uw.win_click(search_butt)

    status_num = uw.page_get_num(page)
    VERIFY(status_num==1, 'Not Such Unique Security') 

    grid = status_num = uw.get_child_chk(page, automation_id='59661', ctrl_type='Pane', deep=10, use_re=True)
    # hide
    uw.win_click(grid, mode='grid_row1')
    mouse.click('right')
    sleep(0.25)

    uw.popup_reply(app.wtop, 'New#Care Order')          # Il popup viene generato sotto level top - anche il sotto menu
    uw.page_save(page, 'security_search', time_tag=True)
    uw.page_close(page, )

def do_new_care_order(arg):
    dlg = uw.get_child_chk(app.wtop, name="New Care Order.*", ctrl_type="Pane", use_re=1)
    uw.win_move(dlg, 333,333)                              # davanti alla toolbar sembra creare problemi a step successivo
    dlg.set_focus()
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
    order = ul.GetLogRows(log_path, 'CLIENT_ORDER', 'ComplianceText', mytag, start_time, retry = 10, wait_s = 1)

    VERIFY(order, 'Order not Found')

    uw.win_close(dlg)                                       # davanti alla toolbar sembra creare problemi a step successivo
    
    return order['fields']['OrderID']

def do_select_order(arg):
    order_id = arg
    print(f'order_id: {order_id}')
    app.click_ribbon_butt('Trading', 'Orders')
    
    page = uw.get_child_chk(app.wtop, name='Orders.*', ctrl_type='Pane', use_re=1, deep=2)
    uw.win_resize(page, 1400, 450)
    
    edit = uw.get_child_chk(page, name='Order ID', ctrl_type='Edit', deep=5)  
    uw.edit_set(edit, order_id)

    butt = uw.get_child_chk(page, name='Apply', ctrl_type='Button', deep=5)  
    uw.win_click(butt)

    status_num = uw.page_get_num(page)
    VERIFY(status_num==1, 'Order Selection Failed') 

    uw.page_save(page, 'order_filtered', time_tag=True)

def do_grid_sample(arg):                         
    app.click_ribbon_butt('Trading', 'Security Browser')                            # todo: Gia una aperta : selezionare l utima ?
    page = uw.get_child_chk(app.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    grid = uw.page_get_grid(page)

    uw.win_resize(page, 1400, 450)

    #search_edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
    #search_butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
    #uw.edit_set(edit, '')
    #uw.win_click(butt, wait_end=.5)

    treekey = f'{COH_EXC} - {COH_MRK}'
    item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
    uw.win_click(item)

    # Esempio Get sheet info
    ug.set_show_all_2(app.wtop, grid)
    grid_mng = ug.create_by_win(grid)
    
    # esempio scroll
    ug.scroll_home(grid_mng)

    # esempio sort
    ug.set_sort(grid_mng,'default')
    ug.set_sort(grid_mng, [['Section','DESC'],['Security Ref.','ASC']])

    #esempio Import Rows
    ug.import_rows(grid_mng, 85, mode='row')
    
    # esempio Data Search-Use
    print (f'Collected Rows: {grid_mng.get_row_num()}')
    sel = grid_mng.search_first_match({"Description": COH_SEC})             # piu segmenti con , 
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
def robot_run(fun_name:str, arg:str='', options=[], session='hang'):
    def manage_session(session):
        if session=='new':
            app.launch_app(COH_PATH)
        else:
            app.hang_app(COH_PATH)
        if session=='kill':
            uw.session_close(app.wtop, wait_init=1, wait_end=1, logoff=True)
    def verify_session(session):
        if session=='kill':
            exist = 0
            try:
                app.hang_app(COH_PATH)
                exist=1
            except Exception as e:
                pass
            VERIFY(not exist, 'Close Session Failed. Process still Exists')
        else:
            VERIFY(app.app and app.wtop, "Hang or New Session Failed")
            app.wtop.set_focus()
    try:
        opt.set(options)
        print(f'Test Options: {options}')
        manage_session(session)
        verify_session(session)
        func = globals().get(fun_name)
        result = func(arg)
        return ROBOT_RES('ok', result)
    except Exception as e:
        message = str(e)
        DUMP(message)
        return ROBOT_RES('no', message) 
    
    
######################################################
# Main DEBUG 

    
if __name__ == '__main__':
    opts = {'speed': '110', 'run': 'local', 'reuse_wsp': 'yes', 'save_wsp_onclose': 'yes', 'close_all_pages': 'yes'}
    opt.set(opts)
    select = 1
    if (select==1):
        print(robot_run('do_search_security', '', opts,'hang') )
        #env.hang_app(COH_PATH)
        #do_grid_sample('')
    if (select==2):
        app.hang_app(COH_PATH)
        do_start_dialog('')


