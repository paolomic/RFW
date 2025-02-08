import keyboard
import mouse
import time

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

from utl_app import env
from utl_win import sleep, ROBOT_RES
from utl_verifier import VERIFY, RAISE, DUMP
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud




######################################################
###  Session Parameter
#region 

COH_PATH =          r'C:\work\disks\D\COH_x64\bin\Coherence.exe'
COH_TITLE_PATT=     "Starting Coherence"
COH_ADDIN=           ['MetaMarket','UserPages']

COH_WSP=            r"C:\work\disks\D\wsp_c\127_28000.wsp4"

COH_EXC=            'BIT'
COH_MRK=            'MTA'
COH_SEC=            'AUTOGRILL SPA'
COH_PRICE =         '95.01'
COH_QTY =           '100'
COH_ALIAS =         'KATIA'
COH_CLIENTID =      'MARI'
COH_CLIENTACC =     'TEST'

#endregion


######################################################
### Local Test - Session 3

def run_session_TEST(): 
    env.hang_app(COH_PATH)
    page = uw.get_child_chk(env.wtop, name='Orders', ctrl_type='Pane', deep=3)
    grid = uw.get_child_chk(page, name='StingrayGrid', deep=8)
    #print(f'page {page}, grid{grid}')
    grid_mng = ug.create_by_win(grid)
    return 'ok'
    
######################################################
### Test: New Session

def robot_launch_new_session(arg):
    def do():
        VERIFY(env.app and env.wtop, "New Session Failed")
    
    try:
        env.launch_app(COH_PATH)
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 
    
######################################################
### Test: Start Dialog
    
def robot_start_dialog(arg):
    def do():
        VERIFY(env.app and env.wtop, "Hang Session Failed")
        edit = uw.get_child_chk(env.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, COH_WSP)

        list = uw.get_child_chk(env.wtop, name='Import From', ctrl_type='List', deep=3)
        uw.list_check(list, '*', False)
        uw.list_check(list, arg, True)

        butt = uw.get_child_chk(env.wtop, automation_id='1', ctrl_type='Button', deep=3)
        is_create = butt.window_text()=='Create'
        uw.win_click(butt, wait_end=0.5)
        uw.warning_replay(env.wtop, 'This workspace has not been closed properly', 'No')

        sleep(3.5)                                                                         # todo : Smart Wait                     
        env.reload()  
        
    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: Setting Dialog

def robot_setting_init(arg):
    def do():
        butt = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Button', deep=3)
        uw.win_click(butt, wait_end=0.5)

        pane = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Pane', deep=3)

        list = uw.get_child_chk(pane, automation_id='103', ctrl_type='List', deep=3)
        uw.list_select(list, "MetaMarket")

        trace = uw.get_child_chk(pane, name='Trace Level', ctrl_type='Custom', deep=3)
        uw.win_click(trace, mode='combo')

        #sleep(.25)
        #ud.dump_uia_tree(env.wtop)         # non c'e' lista popup

        uw.hide_select(-1)                  # Todo Control Inside
        keyboard.press("enter")
        sleep(.25)
        keyboard.press("enter")
        sleep(.25)

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: Start Connection

def robot_start_connections(arg):
    def do():
        addins = ['MetaMarket']                                                     # TODO pass form Robot ?
        for addin in addins:
            butt = env.select_ribbon_butt(addin, 'Auto Connect')
            if not uw.butt_is_checked(butt):
                uw.win_click(butt)

        butt = env.select_ribbon_butt('Home', 'Auto Connect')
        if not uw.butt_is_checked(butt):
            uw.win_click(butt)

        if env.wait_conn_ready(to_sec=30, to_err_sec=5, delay=2):
            print ('Connection Ready')
        else:
            RAISE("Connection Fail")

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: Security Browser

def robot_security_browser(arg):
    def do():
         # la pg viene generata sotto main-node coherence
        page = uw.get_child_chk(env.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=1)
        uw.win_activate(page)                                               # todo portare in front
        #uw.win_resize(page, 600,400)

        edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
        uw.edit_set(edit, '')

        butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
        uw.win_click(butt, wait_end=.5)

        treekey = f'{COH_EXC} - {COH_MRK}'
        item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
        uw.win_click(item)

        edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # POTEVO USARE -1 
        uw.edit_set(edit, COH_SEC)

        butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
        uw.win_click(butt)

        status_num = uw.get_child_chk(page, name='No. of Rows: .*', ctrl_type='Text', deep=10, use_re=True)
        print(f'status_num {status_num}')
        VERIFY(status_num.window_text()=='No. of Rows: 1','Security not Unique')

        grid = status_num = uw.get_child_chk(page, automation_id='59661', ctrl_type='Pane', deep=10, use_re=True)
        # hide
        uw.win_click(grid, mode='grid_row1')
        mouse.click('right')
        sleep(0.25)

        uw.popup_reply(env.wtop, 'New#Care Order')          # Il popup viene generato sotto level top - anche il sotto menu

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: New Care Order

def robot_new_care_order(arg):
    def do():
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
            
        start_time = ul.get_now_sec()                           # Note
        mytag = f'pwa_{start_time.replace(":","_")}' 
        edit = uw.get_child_chk(dlgadv, automation_id='12954')  
        uw.edit_set(edit, mytag)

        uw.win_close(dlgadv.handle)

        but = uw.get_child_chk(dlg, automation_id='1')          # Buy     
        uw.win_click(but)

        log_path = uw.get_log_path(COH_WSP, 'MetaMarket')
        order = ul.GetLogRows(log_path, 'CLIENT_ORDER', 'ComplianceText', mytag, start_time, retry = 4, wait_s = 1)

        if (not order):
            RAISE("Order not Found")
        
        return order['fields']['OrderID']

    try:
        env.hang_app(COH_PATH)
        orderid = do()
        return ROBOT_RES('ok', orderid)                 # return orderid to robot   
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: Select Order

def robot_select_order(arg):
    def do(order_id):
        env.click_ribbon_butt('Trading', 'Orders')
        page = uw.get_child_chk(env.wtop, name='Orders.*', ctrl_type='Pane', use_re=1, deep=2)
        
        edit = uw.get_child_chk(page, name='Order ID', ctrl_type='Edit', deep=5)  
        uw.edit_set(edit, order_id)

        butt = uw.get_child_chk(page, name='Apply', ctrl_type='Button', deep=5)  
        uw.win_click(butt)

    try:
        env.hang_app(COH_PATH)
        do(arg)
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

######################################################
### Test: Grid Sample Sort Import

def robot_grid_sample(arg):
    def do():
        #env.click_ribbon_butt('Trading', 'Security Browser')
        page = uw.get_child_chk(env.wtop, name='Security Browser', ctrl_type='Pane', deep=3)
        grid = uw.get_child_chk(page, name='StingrayGrid', deep=9)
        #print(f'page {page}, grid{grid}')
        
        edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
        uw.edit_set(edit, '')

        butt = uw.get_child_chk(page, name='Search', ctrl_type='Button', deep=10)
        uw.win_click(butt, wait_end=.5)

        treekey = f'{COH_EXC} - {COH_MRK}'
        item = uw.get_child_chk(page, name=treekey, ctrl_type='TreeItem', deep=10) 
        uw.win_click(item)

        # Esempio Get sheet info

        grid_mng = ug.create_by_win(grid)
        ug.set_show_all(grid_mng)

        # esempio scroll
        ug.scroll_home(grid_mng)

        # esempio sort
        ug.set_sort(grid_mng,'default')
        ug.set_sort(grid_mng, [['Section','DESC'],['Security Ref.','ASC']])

        #esempio LoaD
        ug.import_rows(grid_mng, 50, mode='row')
        
        # esempio Data Search-Use
        print (f'Collected Rows: {grid_mng.get_row_num()}')
        sel = grid_mng.search_first_match({"Security Ref.": "ABT"})      # piu segmenti con , 
        VERIFY(sel, 'Security not Found')
        #print(f'Find Row: {sel}')
        print(f'Find {1 if sel else 0} Row')
        print(f'Security Status {sel["Status"]}')

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        print(str(e))
        return ROBOT_RES('no', str(e)) 

######################################################
### Main - Local Test

if __name__ == '__main__':
    select = 3

    if (select==1):
        print(run_session_TEST())
    if (select==2):
        pass
    if (select==3):
        print(robot_new_care_order(None))