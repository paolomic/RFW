import keyboard
import mouse
import webbrowser 
import subprocess
import time

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl as utl
from utl_config import config
from utl_app import env
from utl_web import webapp, WebTable, WebBondDlg
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES

import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud


######################################################
#region - Robot Coherence 

def do_coh_new_session(arg):
    path_wsp = Path(config.get('coh.wsp'))
    if (path_wsp.exists() and not config.get('opt.reuse_wsp')=='yes'):
        print('Remove Workspace...')
        path_wsp.unlink()
        VERIFY(not path_wsp.exists(), 'Wsp Exist')
    #path_wsp_folder = Path(config.get('coh.wsp').replace('.wsp4', '.wsp4_wrk'))
    #if (path_wsp_folder.exists()):
    #    path_wsp_folder.rmdir()
    #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

def do_coh_start_dialog(arg):
    edit = uw.get_child_chk(env.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
    uw.edit_set(edit, config.get('coh.wsp'))

    list = uw.get_child_chk(env.wtop, name='Import From', ctrl_type='List', deep=3)
    uw.list_check(list, '*', False)
    uw.list_check(list, config.get('coh.addins'), True)

    butt = uw.get_child_chk(env.wtop, automation_id='1', ctrl_type='Button', deep=3)
    if not config.get('opt.reuse_wsp')=='yes':
        VERIFY(butt.window_text()=='Create', 'Can`t Create New Workspace')

    uw.win_click(butt, wait_end=0.5)
    uw.warning_replay('This workspace has not been closed properly', 'No')
                                                                                   
    env.reload()                                                                            # Smart Wait for new Main Frame   
        
def do_coh_setting_init(arg):
    butt = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Button', deep=4)          # Settings gia aperto se New Wsp
    uw.win_click(butt)

    pane = uw.get_child_chk(env.wtop, name='Settings', ctrl_type='Pane', deep=3)
    list = uw.get_child_chk(pane, automation_id='103', ctrl_type='List', deep=3)

    ### Connection  - Disable se connection Ready
    try:
        edit = uw.get_child_chk(pane, name='Host', ctrl_type='Edit', deep=1)
        uw.edit_set(edit, config.get('coh.primary'))
        edit = uw.get_child_chk(pane, name='Port', ctrl_type='Edit', deep=1)
        uw.edit_set(edit, config.get('coh.port'))
        edit = uw.get_child_chk(pane, name='User name', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, config.get('coh.user'))
        edit = uw.get_child_chk(pane, automation_id='11303', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, config.get('coh.pass'))
        
        if config.get('coh.band_save'):
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

def do_coh_start_connections(arg):
    if config.get('opt.close_all_pages')=='yes':
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

def do_coh_prepare_session(arg):
    do_coh_new_session(arg)
    do_coh_start_dialog(arg)
    do_coh_setting_init(arg)
    do_coh_start_connections(arg)

def do_coh_reply(arg):
    dlg_rfq = uw.get_child_chk(env.wtop, name=r"RFQ Outright \[CANDEAL\/BOND\] \[\d+\]", ctrl_type='Pane', deep=1, use_re=1)  
    butt = uw.get_child_chk(dlg_rfq, name='Done', ctrl_type='Button', deep=1)  
    utl.sleep_progress(10)
    uw.win_click(butt)
#endregion


######################################################
#region - Robot Web 

def do_web_login_session(arg):
    webapp.launch_url(config.get('web.url'))
    edit = uw.get_child_chk(webapp.doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, config.get('web.user'))
    edit = uw.get_child_chk(webapp.doc, name='PASSWORD.', automation_id='password', ctrl_type='Edit', use_re=1)
    uw.edit_set(edit, config.get('web.pass'))
    keyboard.press_and_release('esc')
    butt = uw.get_child_chk(webapp.doc, name='LOGIN.*', ctrl_type='Button', use_re=1)
    uw.win_click(butt)
    sleep(2)                   # todo - smart wait

    try:
        wrn = uw.get_child_chk(webapp.doc, name='Notifications popup are disabled')
        butt = uw.get_child_chk(wrn, name='OK', deep=2)
        uw.win_click(butt)
    except:
        pass

def do_web_open_rfq(arg):
    webapp.hang_main()
    butt = uw.get_child_chk(webapp.doc, name='', deep=2)  # clear - todo AutomationId
    uw.win_click(butt, wait_end=.5)

    combo = uw.get_child_chk(webapp.doc, name='Search Security', ctrl_type='ComboBox', deep=2)  # clear - todo AutomationId
    uw.edit_set(combo, config.get('web.sec'), wait_end=1)

    butt = uw.get_child_chk(webapp.doc, name='', deep=2)  # insert - todo AutomationId
    uw.win_click(butt, wait_end=.5)

    butt = uw.get_child_chk(webapp.doc, name='NEW RFQ', ctrl_type='Button', deep=2)  # insert - todo AutomationId
    uw.win_click(butt, wait_end=.5)
    
    uw.sleep(1.5)      # new windows opening

def do_web_send_rfq(arg):
    rfq = webapp.hang_rfq()
    
    #print(ud.dump_uia_tree(table))

    combo = uw.get_child_chk(rfq, name='-', ctrl_type='ComboBox', deep=2)   # mancano locator
    uw.win_click(combo)
    uw.edit_set(combo, 'My offer')

    label = uw.get_child_chk(rfq, name='QTY', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')                  # todo mancano Key
    uw.edit_set_manual(combo, config.get('web.qty'), reset=1)               # usa keyboard

    label = uw.get_child_chk(rfq, name='PRICE', ctrl_type='Text')
    combo = uw.get_child_after(label, ctrl_type='Spinner')
    uw.edit_set_manual(combo, config.get('web.price'), reset=1)             # usa keyboard
   
    butt = uw.get_child_chk(rfq, name='RBC', ctrl_type='Button')
    uw.win_click(butt)

    butt = uw.get_child_chk(rfq, name='SEND', ctrl_type='Button')
    uw.win_click(butt)

    sleep(1)

def do_web_manage_rfq(arg):

    rfq = webapp.hang_rfq()
    dlg_bond = WebBondDlg(rfq)

    while dlg_bond.is_live():
        str_time = dlg_bond.get_time()
        print(f'RFQ Active... {str_time}')
        print(print(f'Answer From {dlg_bond.get_answer(short=1)}'))
        utl.sleep_progress(5)

    sleep(0.5)

    str_state = dlg_bond.get_final_state()
    print(f'Rfq Ended - Info {str_state}')

    all_answ = dlg_bond.get_answer()
    print(f'No.Row:{len(all_answ)}')
    print(all_answ)

    VERIFY(str_state=='DONE', "RFQ Status Unexpected")

#endregion

######################################################
# Generic Caller

# todo differenziare connection web e coh

#conn 'coh:hang,kill web:new,run'


def robot_run(fun_name:str, arg:str, cfg_file, conn=''):
    def manage_conn(event):
        env.manage_conn(event, conn)
        webapp.manage_conn(event, conn)
    try:
        config.load(cfg_file)
        manage_conn('start')
        func = globals().get(fun_name)
        result = func(arg)
        manage_conn('exit')
        return ROBOT_RES('ok', result)
    except Exception as e:
        message = str(e)
        DUMP(message)
        return ROBOT_RES('no', message) 
    
    
######################################################
# Main - DEBUG 

    
if __name__ == '__main__':
    cfg_file = r'.\utils\test\test_cd_rfq.json'
    select = 1
    if (select==1):
        #print(robot_run('do_login_session', '', cfg_file, '') )
        #print(robot_run('do_open_rfq', '', cfg_file, '') )
        #print(robot_run('do_send_rfq', '', cfg_file, '') )
        #print(robot_run('do_manage_rfq', '', cfg_file, '') )
        #print(robot_run('do_coh_new_session', '', cfg_file, 'new') )
        #print(robot_run('do_coh_setting_init', '', cfg_file, 'hang') )
        print(robot_run('do_coh_reply', '', cfg_file, 'coh:hang') )
        pass
    if (select==2):
        do_manage_rfq('')
        #do_login_session('')

