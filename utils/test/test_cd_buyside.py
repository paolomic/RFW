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
from utl_app import env, opt
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




def do_login_session(arg):
    
    """ 
    subprocess.run(["start", "chrome", "--new-window", WEB_URL], shell=True)
    sleep(1)
    """ 
    
    """ 
    brow = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)
    VERIFY(brow, 'Error: Open Browser')
    doc = uw.get_child(brow, automation_id='150784384')
    edit = uw.get_child(doc, name='USERNAME.', automation_id='username', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, 'OP1@CUST1')
    edit = uw.get_child(doc, name='PASSWORD.', automation_id='password', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, '*')
    butt = uw.get_child(doc, name='LOGIN.*', ctrl_type='Button', use_re=1)
    uw.win_click(butt)
    sleep(2)                   # smart wait
     check popup

    try:
        wrn = uw.get_child(doc, name='Notifications popup are disabled')
        butt = uw.get_child(wrn, name='OK', deep=2)
        uw.win_click(butt)
    except:
        pass
    """ 


    """ 
    butt = uw.get_child(doc, name='', deep=2)  # clear - todo AutomationId
    uw.win_click(butt)

    combo = uw.get_child(doc, name='Search Security', ctrl_type='ComboBox', deep=2)  # clear - todo AutomationId
    uw.edit_set(combo, 'BCECN 3.350 03/12/2025')

    butt = uw.get_child(doc, name='', deep=2)  # insert - todo AutomationId
    uw.win_click(butt)

    butt = uw.get_child(doc, name='NEW RFQ', ctrl_type='Button', deep=2)  # insert - todo AutomationId
    uw.win_click(butt)
    
    sleep(1.5)      # new windows opening

    """    
    rfq = uw.get_main_wnd('New Bond RFQ.*Google Chrome.*', use_re=1)
    table = uw.get_child(rfq, ctrl_type='Table', deep=2)
    grp = uw.get_child(table, ctrl_type='Group', deep=1)        # group combo type
    print(f'grp {grp}')
    combo = uw.get_child(grp, name='-', ctrl_type='ComboBox')
    uw.win_click(combo)
    uw.edit_set(combo, 'My offer')

    #print(ud.dump_uia_tree(table))
    
    label = uw.get_child(table, name='QTY', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')              # todo mancano Key
    uw.edit_set_manual(combo, WEB_QTY, reset=1)         # usa keyboard

    label = uw.get_child(table, name='PRICE', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')
    uw.edit_set_manual(combo, WEB_PRICE, reset=1)         # usa keyboard
   
    butt = uw.get_child(table, name='RBC', ctrl_type='Button')
    uw.win_click(butt)

    butt = uw.get_child(table, name='SEND', ctrl_type='Button')
    uw.win_click(butt)

    sleep(1)
    # need reload ?
    rfq = uw.get_main_wnd('New Bond RFQ.*Google Chrome.*', use_re=1)
    table = uw.get_child(rfq, ctrl_type='Table', deep=2)

#endregion


######################################################
# Generic Caller

# todo differenziare connection web e coh


def robot_run(fun_name:str, arg:str='', options=[], session='hang'):
    def manage_session(session):
        if session=='new':
            env.launch_app(COH_PATH)
        else:
            env.hang_app(COH_PATH)
        if session=='kill':
            uw.session_close(env.wtop, wait_init=1, wait_end=1, logoff=True)
    def verify_session(session):
        pass
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
    select = 2
    if (select==1):
        print(robot_run('do_login_session', '', opts, 'new') )
        #env.hang_app(COH_PATH)
        #do_grid_sample('')
    if (select==2):
        do_login_session('')

