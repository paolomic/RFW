import keyboard
import mouse
import time
import os
import psutil
#TODO Spostare questo py in tests/modules (problema include)



#strpath = r'C:\work\disks\D\prog\RFW\utils'
#sys.path.append(strpath) 

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

from pywinauto import Application


######################################################
###  Session Parameter
#region 

#COH_SETUP = r'C:\Users\Paolo.Michetti\OneDrive - ION\Desktop\CanDeal_evolutionSetup_x64_25_6.0.0d3.exe'
COH_SETUP = r'C:\Users\Paolo.Michetti\OneDrive - ION\Desktop\setup.exe'

#endregion
class AppEnv:
    #private
    setup_path = None
    setup_exe = None

    app = None
    wtop = None

    def start(self):
        print('Starting new instance...')
        self.app = Application(backend="uia").start(self.setup_path)
        print(f'app {self.app}')
        time.sleep(3)                                               # TODO attesa attiva
        self.wtop = self.app.top_window()
        print(f'wtop {self.wtop}')

    def connect(self):
        print('Connecting instance...')
        self.app = Application(backend="uia").connect(path=self.setup_exe)
        self.wtop = env.app.top_window()

    def __init__(self, setup_path):
        self.setup_path = setup_path
        self.setup_exe = os.path.basename(self.setup_path)

env = AppEnv(COH_SETUP)

######################################################
### Robot Operations
#region 
def do_setup(arg):
    VERIFY(env.wtop.window_text()=='CanDeal evolution Setup', 'Setup Starting Failed')

def do_go(arg):     # Nota: Problemi a riagganciare il processo - tutto 1 sessione
    butt = uw.get_child_chk(env.wtop, name='Next >', automation_id='1')
    print(f'butt {butt}')
    uw.win_click(butt)
    pass



#endregion


######################################################
# Generic Caller
def robot_run(fun_name:str, arg:str='', options=[], session='hang'):
    def manage_session(session):
        if session=='new':
           env.start()
        else:
            env.connect()
        if session=='kill':
            pass
            #uw.session_close(env.wtop, wait_init=1, wait_end=1, logoff=True)
    def verify_session(session):
        if session=='kill':
            pass
        else:
            VERIFY(env.app and env.wtop, "Hang or New Session Failed")
            env.wtop.set_focus()

    try:
        opt.set(options)
        print(f'Test Options: {options}')
        manage_session(session)
        verify_session(session)
        func = globals().get(fun_name)
        result = func(arg)
        return ROBOT_RES('ok', result)
    except Exception as e:
        return ROBOT_RES('no', str(e)) 
    
    
######################################################
# Main DEBUG 

    
if __name__ == '__main__':
    opts = {'speed': '110', 'run': 'local', 'reuse_wsp': 'yes', 'save_wsp_onclose': 'yes', 'close_all_pages': 'yes'}
    opt.set(opts)
    
    select = 1
    if (select==1):
        #print(robot_run('do_setup', '', opts,'new') )
        print(robot_run('do_go', '', opts,'hang') )
      
    if (select==2):
        pass
    if (select==3):
        print('Connecting instance...')
        app = Application(backend="uia").connect(process=21696)
        print(f'app {app}')
        wtop = env.app.top_window()
        print(f'app {app}')
    if select==4:
            for proc in psutil.process_iter(['pid', 'name']):
                print(proc.info)




