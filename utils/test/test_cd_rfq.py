####################################################################
# TEST CD_RFQ
####################################################################

#region - import

import keyboard
import mouse

# Import utils
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

# util modules
import utl as utl
from utl_config import config
from utl_app import app
from utl_web import wapp
from utl_verifier import CLEAR, VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_run as ur
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud

# page modules
from page_console           import PageSettings
from page_addin_sellside    import DlgRfqBond
from page_web               import WebDlgRfqBond

#endregion

def do_prepare_test(arg):
    ur.terminate_sessions()
    CLEAR(5)
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
    app.connection(start=True, addins = ['MetaMarket'], timeout=120)

def do_coh_prepare_session(arg):
    do_coh_new_session(arg)
    do_coh_start_dialog(arg)
    do_coh_setting_init(arg)
    do_coh_start_connections(arg)

def do_coh_reply(arg):
    dlg_rfq = DlgRfqBond()
    utl.sleep_progress(10)  # suspance ...
    dlg_rfq.press('Done')

#endregion

####################################################################
#region - Robot Web 

filter_set_security_retray = utl.retry_fun(retry_delay=20, retry_timeout=2)(wapp.filter_set_security)



def do_web_login_session(arg):
    retry_fun = utl.retry_fun(retry_timeout=120, retry_delay=2) (wapp.web_boot)
    retry_fun()
    
def do_web_open_rfq(arg):
    def attempt():
        try:
            wapp.hang_main()
            wapp.filter_clear()                                             # todo: mancano locators
            filter_set_security_retray(config.get('web.sec'))               # todo: mancano locators
            wapp.new_rfq()                                                  # todo: mancano locators
            return True
        except:
            # chiusura
            return None
    
    retry_fun = utl.retry_fun(retry_timeout=60, retry_delay=2) (attempt)
    retry_fun()
    
    sleep(1.5)                                                      # new windows opening - todo smart_wait ?

def do_web_send_rfq(arg):
    wapp.hang_main()
    rfq = WebDlgRfqBond()
    rfq.set_combo('My offer')
    rfq.set_price(config.get('web.price'))
    rfq.set_qty(config.get('web.qty'))
    rfq.set_dealer('RBC')
    rfq.set_dealer('CBMO')
    rfq.send()
    sleep(10)    
    rfq = WebDlgRfqBond()                                      # reload trading mode
    VERIFY(rfq.is_live(), 'Rfq Dialog non Stared')

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


def robot_run(req:dict, cfg_file:str):
    return ur.robot_run_3(globals().get(req['fun']), req, cfg_file)             # ha il suo exception handler
        






######################################################
# Main - DEBUG 


if __name__ == '__main__':
    
    select = 1
    if (select==1):
        cfg_file = r'.\utils\test\test_cd_rfq.json'
        req = {'fun':'do_web_open_rfq',    'arg':'',    'coh':'',    'web':'',   'timeout':'300' }       #parte il controller
        #call
        print(robot_run(req, cfg_file))
        pass
    if (select==2):
        do_web_manage_rfq('')
        #do_web_login_session('')
    if (select==3):
        config.load(cfg_file)
        wapp.launch_url(config.get('web.url'))
        edit = uw.get_child_retry(wapp.doc, name='USERNAMEx.*', automation_id='username', ctrl_type='Edit', use_re=1, retry_timeout=16)
        print (edit)
        pass

