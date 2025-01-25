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

COH_PATH =          r'C:\work\disks\D\COH_x64\bin\Coherence.exe'                # TODO: JSon File ?
COH_ADDIN=           ['MetaMarket','UserPages']

COH_WSP=            r"C:\work\disks\D\wsp_c\test.wsp4"
COH_PRIMARY=        '192.168.200.127'         
COH_PORT=           '28000'         
COH_USER=           'MARI'         
COH_PASS=           '*'         
COH_BAND=           True

COH_EXC=            'BIT'
COH_MRK=            'MTA'
COH_SEC=            'AUTOGRILL SPA'
COH_PRICE =         '95.01'
COH_QTY =           '100'
COH_ALIAS =         'KATIA'
COH_CLIENTID =      'MARI'
COH_CLIENTACC =     'TEST'

#endregion



### Robot Funz.

def robot_new_session(arg):
    def do():
        VERIFY(env.app and env.wtop, "New Session Failed")
        path_wsp = Path(COH_WSP)
        if (path_wsp.exists()):
            path_wsp.unlink()
        VERIFY(not path_wsp.exists(), 'Wsp Exist')
        #path_wsp_folder = Path(COH_WSP.replace('.wsp4', '.wsp4_wrk'))
        #if (path_wsp_folder.exists()):
        #    path_wsp_folder.rmdir()
        #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')
        
    try:
        env.launch_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

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
        VERIFY(is_create, 'Can`t Create New Workspace')

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

def robot_setting_init(arg):
    def do():

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
        
        if COH_BAND:
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

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

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

        if uw.statusbar_wait(env.st_bar, 'Ready', attempt=15, delay=2):             # Wait for Connection Ready
            print ('Connection Ready')
        else:
            RAISE("Connection Fail")

    try:
        env.hang_app(COH_PATH)
        do()
        return ROBOT_RES('ok')                  
    except Exception as e:
        return ROBOT_RES('no', str(e)) 

def robot_search_security(arg):
    def do():
        # la pg viene generata sotto main-node coherence
        env.click_ribbon_butt('Trading', 'Security Browser')
        page = uw.get_child_chk(env.wtop, name='Security Browser', ctrl_type='Pane', deep=3)
        grid = uw.get_child_chk(page, name='StingrayGrid', deep=9)

        #edit = uw.get_child_chk(page, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
        #uw.edit_set(edit, '')

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
        assert status_num.window_text()=='No. of Rows: 1'       # UNIQUE 

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



############## 
# END DEBUG 

def prova(arg):
    env.hang_app(COH_PATH)
    page = uw.get_child_chk(env.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
    #uw.win_move(page, 12, 12)
    uw.win_resize(page, 444, 444)
    

if __name__ == '__main__':
    select = 1

if (select==1):
    print(prova(''))


