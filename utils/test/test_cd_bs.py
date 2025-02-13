import keyboard
import mouse
import webbrowser 
import subprocess

#TODO Spostare questo py in tests/modules (problema include)


# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl
from utl_app import env, wenv, opt
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud


######################################################
###  Session Parameter
#region 

WEB_URL =               r'http://10.91.204.20/login'

WEB_SEC =               'BCECN 3.350 03/12/2025'
WEB_QTY =               '2000'
WEB_PRICE =             '101.34'

#endregion


######################################################
### Robot Operations
#region 

def do_login_session(new=False):
    (brw, doc) = wenv.launch_url(WEB_URL)
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
    (brw, doc) = wenv.hang_main()
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
    (rfq, table, grp) = wenv.hang_rfq()

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
    (rfq, table, grp) = wenv.hang_rfq()

    time = None
    while not uw.get_child(table, name='.*EXPIRED.*', use_re=1):
        try:
            if not time:
                time = uw.get_child(table, name=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', use_re=1, deep=6)
            print(f'table runnig... {time.window_text()}')
        except:
            break

        for i in range(6):
            print('.', end='', flush=True)
            uw.sleep(1)
        print('')

    sleep(1)
        
    print('Rfq EXPIRED')



######################################################
# Generic Caller

# todo differenziare connection web e coh


def robot_run(fun_name:str, arg:str='', options=[], s_op=''):
    def manage_session(s_op):
        pass
    def verify_session(ope):
        pass
    try:
        opt.set(options)
        print(f'Test Options: {options}')
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
    opts = {'speed': '110', 'run': 'local', 'reuse_wsp': 'yes', 'save_wsp_onclose': 'yes', 'close_all_pages': 'yes'}
    opt.set(opts)
    select = 0
    if (select==1):
        #print(robot_run('do_login_session', '', opts, '') )
        #print(robot_run('do_open_rfq', '', opts, '') )
        #print(robot_run('do_send_rfq', '', opts, '') )
        #print(robot_run('do_manage_rfq', '', opts, '') )
        #do_grid_sample('')
        pass
    if (select==2):
        wenv.hang_app()
        do_login_session('')

