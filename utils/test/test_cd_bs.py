import keyboard
import mouse
import webbrowser 
import subprocess
import time

#TODO Spostare questo py in tests/modules (problema include)


# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl
from utl_app import env, opt
from utl_web import webapp, WebTable, WebBondDlg
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES

import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud


######################################################
###  Session Coherence Parameter
COH_PATH =              r'D:\COH_x64_CANDEAL_NEXT\bin\Coherence.exe'                # TODO: JSon File ?
COH_ADDIN=              ['MetaMarket','RFQ Sell Side', 'UserPages']

COH_WSP=                r"D:\wsp_cd\robot_test.wsp4"
COH_PRIMARY=            '10.91.204.14'         
COH_PORT=               '27000'         
COH_USER=               'AASMAH@RBC'         
COH_PASS=               '*'         
COH_BAND_SAVE=           True

#COH_EXC=                'BIT'
#COH_MRK=                'MTA'
#COH_SEC=                'AUTOGRILL SPA'
#COH_PRICE =             '95.01'
#COH_QTY =               '100'
#COH_ALIAS =             'KATIA'
#COH_CLIENTID =          'MARI'
#COH_CLIENTACC =         'TEST'


######################################################
###  Session Web Parameter
#region 

WEB_URL =               r'http://10.91.204.20/login'

WEB_SEC =               'BCECN 3.350 03/12/2025'
WEB_QTY =               '2000'
WEB_PRICE =             '101.34'

#endregion



######################################################
### Robot Coherence Operations
#region 
def do_ss_new_session(arg):
    path_wsp = Path(COH_WSP)
    if (path_wsp.exists() and not opt.get('reuse_wsp')=='yes'):
        print('Remove Workspace...')
        path_wsp.unlink()
        VERIFY(not path_wsp.exists(), 'Wsp Exist')
    #path_wsp_folder = Path(COH_WSP.replace('.wsp4', '.wsp4_wrk'))
    #if (path_wsp_folder.exists()):
    #    path_wsp_folder.rmdir()
    #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

def do_ss_start_dialog(arg):
    edit = uw.get_child_chk(env.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, COH_WSP)

    list = uw.get_child_chk(env.wtop, name='Import From', ctrl_type='List', deep=3)
    uw.list_check(list, '*', False)
    uw.list_check(list, COH_ADDIN, True)

    butt = uw.get_child_chk(env.wtop, automation_id='1', ctrl_type='Button', deep=3)
    if not opt.get('reuse_wsp')=='yes':
        VERIFY(butt.window_text()=='Create', 'Can`t Create New Workspace')

    uw.win_click(butt, wait_end=0.5)
    uw.warning_replay('This workspace has not been closed properly', 'No')
                                                                                   
    env.reload()                                                                            # Smart Wait for new Main Frame   
        
def do_ss_setting_init(arg):
    butt = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Button', deep=4)          # Settings gia aperto se New Wsp
    uw.win_click(butt)

    pane = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Pane', deep=3)
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

def do_ss_start_connections(arg):
    if opt.get('close_all_pages')=='yes':
        uw.page_close_all()
    
    addins = ['MetaMarket']                                                     # TODO pass form Robot ?
    for addin in addins:
        butt = env.select_ribbon_butt(addin, 'Auto Connect')
        if not uw.butt_is_checked(butt):
            uw.win_click(butt)

    butt = env.select_ribbon_butt('Home', 'Auto Connect')
    if not uw.butt_is_checked(butt):
        uw.win_click(butt)

    if env.wait_conn_ready(to_sec=120, to_err_sec=5, delay=2):
        print ('Connection Ready')
    else:
        RAISE("Connection Fail")

def do_ss_reply(arg):
    dlg_rfq = uw.get_child_chk(env.wtop, name='RFQ Outright \[.*\] \[.*\]', ctrl_type='Pane', deep=1, use_re=1)  
    butt = uw.get_child_chk(dlg_rfq, name='Done', ctrl_type='Button', deep=1)  
    uw.win_click(butt)
#endregion


######################################################
### Robot Web Operations
#region 

def do_login_session(arg):
    (brw, doc) = webapp.launch_url(WEB_URL)
    edit = uw.get_child_chk(doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, 'OP1@CUST1')
    edit = uw.get_child_chk(doc, name='PASSWORD.', automation_id='password', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, '*')
    keyboard.press_and_release('esc')
    butt = uw.get_child_chk(doc, name='LOGIN.*', ctrl_type='Button', use_re=1)
    uw.win_click(butt)
    sleep(2)                   # todo - smart wait

    try:
        wrn = uw.get_child_chk(doc, name='Notifications popup are disabled')
        butt = uw.get_child_chk(wrn, name='OK', deep=2)
        uw.win_click(butt)
    except:
        pass

def do_open_rfq(arg):
    (brw, doc) = webapp.hang_main()
    butt = uw.get_child_chk(doc, name='', deep=2)  # clear - todo AutomationId
    uw.win_click(butt)

    combo = uw.get_child_chk(doc, name='Search Security', ctrl_type='ComboBox', deep=2)  # clear - todo AutomationId
    uw.edit_set(combo, WEB_SEC)

    butt = uw.get_child_chk(doc, name='', deep=2)  # insert - todo AutomationId
    uw.win_click(butt)

    butt = uw.get_child_chk(doc, name='NEW RFQ', ctrl_type='Button', deep=2)  # insert - todo AutomationId
    uw.win_click(butt)
    
    uw.sleep(1.5)      # new windows opening

def do_send_rfq(arg):
    (rfq, table, grp) = webapp.hang_rfq()

    combo = uw.get_child_chk(grp, name='-', ctrl_type='ComboBox')
    uw.win_click(combo)
    uw.edit_set(combo, 'My offer')

    #print(ud.dump_uia_tree(table))
    
    label = uw.get_child_chk(table, name='QTY', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')                      # todo mancano Key
    uw.edit_set_manual(combo, WEB_QTY, reset=1)         # usa keyboard

    label = uw.get_child_chk(table, name='PRICE', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')
    uw.edit_set_manual(combo, WEB_PRICE, reset=1)         # usa keyboard
   
    butt = uw.get_child_chk(table, name='RBC', ctrl_type='Button')
    uw.win_click(butt)

    butt = uw.get_child_chk(table, name='SEND', ctrl_type='Button')
    uw.win_click(butt)

    sleep(1)
#endregion

def do_manage_rfq(arg):

    (rfq, table, grp) = webapp.hang_rfq()

    grid = uw.get_child(table, ctrl_type='Table')
    tb = WebTable(grid, load=0)

    dlg_bond = WebBondDlg(table)

    timeout = utl.TimeOut(240)
 
    while True:
        # termination on State
        str_time = dlg_bond.get_time()
        if not str_time:
            break

        print(f'RFQ Active... {str_time}')
        
        # termination on TimeOut
        if timeout.expired():                                #4 min T.O.
            VERIFY(0, 'Timeout Managing Rfq Dialog')
            break

        #while actions
        print(print(f'Answer From {tb.get_answer()}'))

        #polling delay
        for i in range(6):
            print('.', end='', flush=True)
            uw.sleep(1)
        print('')

    sleep(0.5)

    str_state = dlg_bond.get_state()

    print(f'Rfq Ended - Info {str_state}')
    ud.dump_uia_tree_graph(grid)

    tb.load()
    print(f'No.Row:{len(tb.rows)}')
    print(tb.rows)


######################################################
# Generic Caller

# todo differenziare connection web e coh


def robot_run(fun_name:str, arg:str='', options=[], s_op=''):
    def manage_session(session):
        if session=='new':
            env.launch_app(COH_PATH)
        else:
            env.hang_app(COH_PATH)
        if session=='kill':
            uw.session_close(env.wtop, wait_init=1, wait_end=1, logoff=True)
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
            env.wtop.set_focus()
    try:
        opt.set(options)
        print(f'Test Options: {options}')
        if s_op and s_op != 'web':
            manage_session(s_op)   
            verify_session(s_op)
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
    opts = {'speed': '110', 'run': 'local', 'reuse_wsp': 'no', 'save_wsp_onclose': 'yes', 'close_all_pages': 'yes'}
    opt.set(opts)
    select = 1
    if (select==1):
        #print(robot_run('do_login_session', '', opts, '') )
        #print(robot_run('do_open_rfq', '', opts, '') )
        #print(robot_run('do_send_rfq', '', opts, '') )
        #print(robot_run('do_manage_rfq', '', opts, '') )
        #print(robot_run('do_ss_new_session', '', opts, 'new') )
        print(robot_run('do_ss_reply', '', opts, 'hang') )
        pass
    if (select==2):
        do_manage_rfq('')
        #do_login_session('')

