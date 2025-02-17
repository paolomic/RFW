####################################################################
# TEST CD_RFQ
####################################################################

####################################################################
#region - import

import keyboard
import mouse

# Import utils
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl as utl
from utl_config import config
from utl_app import app
from utl_web import wapp
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_run as ur

import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud

from pg_settings import PageSettings
from dg_rfq_bond import DlgRfqBond
from wdg_rfq_bond import WebDlgRfqBond

#endregion

def do_prepare_test(arg):
    ur.terminate_sessions()
    sleep(1)

####################################################################
#region - Robot Coherence 

def do_coh_new_session(arg):
    if not config.get('opt.reuse_wsp')=='yes':
        app.reset_wsp()
    
def do_coh_start_dialog(arg):
    app.start_dialog(config.get('coh.wsp'), config.get('coh.addins'))                                          
    app.reload()                                                                            # Smart Wait for new Main Frame   
    uw.win_move(app.wtop, 8, 8)
    #app.connection(start=False)             # se riuso il wsp stacco la conn
        
def do_coh_setting_init(arg):
    setting_dlg = PageSettings()
    setting_dlg.open()
    ### Connection  - Disable se connection Ready
    setting_dlg.set_platform(config.get('coh.primary'), config.get('coh.port'), 
                             config.get('coh.user'),  config.get('coh.pass'),
                             config.get('coh.band_save') )
    setting_dlg.metamarket('detail')
    setting_dlg.workspace('detail')
    setting_dlg.close()
    

def do_coh_start_connections(arg):
    app.connection(start=True, addins = ['MetaMarket'])

def do_coh_prepare_session(arg):
    do_coh_new_session(arg)
    do_coh_start_dialog(arg)
    do_coh_setting_init(arg)
    do_coh_start_connections(arg)

def do_coh_reply(arg):
    dlg_rfq = DlgRfqBond()
    utl.sleep_progress(20)  # suspance ...
    dlg_rfq.press('Done')

#endregion

####################################################################
#region - Robot Web 

def do_web_login_session(arg):
    wapp.launch_url(config.get('web.url'))
    wapp.set_login_user_password()
    
def do_web_open_rfq(arg):
    wapp.hang_main()

    wapp.filter_clear()                                     # todo: mancano locators
    wapp.filter_set_security(config.get('web.sec'))         # todo: mancano locators
    wapp.new_rfq()                                          # todo: mancano locators
    sleep(1.5)                                              # new windows opening - todo smart_wait ?

def do_web_send_rfq(arg):
    rfq = WebDlgRfqBond()
    rfq.set_combo('My offer')
    rfq.set_price(config.get('web.price'))
    rfq.set_qty(config.get('web.qty'))
    rfq.set_dealer('RBC')
    rfq.set_dealer('CBMO')
    rfq.send()
    sleep(1)

def do_web_manage_rfq(arg):
    dlg_rfq = WebDlgRfqBond()

    while dlg_rfq.is_live():
        str_time = dlg_rfq.get_time()
        print(f'RFQ Active... {str_time}')
        print(print(f'Answer From {dlg_rfq.get_answer(short=1)}'))

        # BuySide Action Here: Accept, ...

        utl.sleep_progress(5)

    str_state = dlg_rfq.get_final_state()
    print(f'Rfq Ended - Info {str_state}')

    all_answ = dlg_rfq.get_answer()
    print(f'No.Row:{len(all_answ)}')
    print(all_answ)

    VERIFY(str_state=='DONE', "RFQ Status Fail")

#endregion

######################################################
# Generic Caller

# todo: piu sessioni coh
# todo: smartwait (web)


def robot_run(fun_name:str, arg:str, cfg_file, conn='', timeout=0):
    func = globals().get(fun_name)
    return ur.robot_run_3(func, arg, cfg_file, conn, timeout)
        
    
######################################################
# Main - DEBUG 

if __name__ == '__main__':
    cfg_file = r'.\utils\test\test_cd_rfq.json'
    select = 3
    if (select==1):
        print(robot_run('do_web_login_session', '', cfg_file, '') )
        #print(robot_run('do_web_open_rfq', '', cfg_file, '') )
        #print(robot_run('do_web_send_rfq', '', cfg_file, '') )
        #print(robot_run('do_web_manage_rfq', '', cfg_file, '') )
        #print(robot_run('do_coh_new_session', '', cfg_file, 'coh:new') )
        #print(robot_run('do_coh_setting_init', '', cfg_file, 'hang') )
        #print(robot_run('do_coh_reply', '', cfg_file, 'coh:hang') )
    if (select==2):
        do_web_manage_rfq('')
        #do_web_login_session('')
    if (select==3):
        #ur.terminate_sessions()
        #print(robot_run('do_prepare_test', '', cfg_file, '', timeout=33) )
        print(robot_run('do_coh_prepare_session', '', cfg_file, 'coh:new', timeout=66) )
        #print(robot_run('do_web_login_session', '', cfg_file, '', timeout=233) )

