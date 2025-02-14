import time
from pywinauto import Application
import subprocess

import utl_win as uw
import utl  as utl

import re
import os
from datetime import datetime, timedelta



from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud
from utl_config import config


##########################################################
#region - Coherence Environment 

class AppEnv:
    app = None
    wtop = None
    #placeholders
    rib_tab = None
    rib_grp = None
    st_bar = None

    #private
    coh_path = None     # to start - file path
    coh_exe = None      # to reconnect - process name

    def reset(self):
        # main
        self.app = None
        self.wtop = None
        #placeholders
        self.rib_tab = None
        self.rib_grp = None
        self.st_bar = None
        #private
        self.coh_path = None
        self.coh_exe = None

    @utl.chrono
    def placeholder(self):
        self.rib_tab = None
        self.rib_grp = None
        self.st_bar = None

        VERIFY(self.app, 'Application handler non Valid')
        VERIFY(self.wtop, 'Windows Application handler non Valid')

        if(not re.match('Starting Coherence.*', self.wtop.window_text())):
            self.rib_grp = uw.get_child_chk(self.wtop, automation_id='59398', ctrl_type='ToolBar', deep=1, verify=False)   # contenuto della tab corrente
            self.rib_tab = uw.get_child_chk(self.rib_grp, name='Ribbon Tabs', ctrl_type='Group', deep=1, verify=False)      # FILE HOME VIWE ....
            self.st_bar = uw.get_child_chk(self.wtop, name='StatusBar', ctrl_type='StatusBar', deep=1, verify=False)        
            

            VERIFY(self.rib_tab, 'Ribbon Tab handler non Valid')
            VERIFY(self.st_bar, 'Ribbon Bar handler non Valid')
            VERIFY(self.st_bar, 'Ribbon Group handler non Valid')

        #print (self)

    def init(self, coh_path): 
        self.reset()
        self.coh_path = coh_path
        self.coh_exe = 'Coherence.exe'

    def launch_app(self, coh_path, unique=True):
        self.init(coh_path)

        if unique:
            found = 0
            try:
                app = Application(backend="uia").connect(path=self.coh_exe)
                found = 1
            except:
                pass
            VERIFY(not found, 'Coherence Already Started')
        
        try:
            print('Starting new instance...')
            self.app = Application(backend="uia").start(self.coh_path)
            sleep(1)                                               # TODO attesa attiva
            self.wtop = self.app.top_window()
        except Exception as e:
            RAISE(f"Start Error: {str(e)}")
            
        #print(f'app {app}')
        #print(f'wtop {wtop}')
        self.placeholder()

    @utl.chrono
    def hang_app(self, coh_path=None, pid=None):
        if not coh_path:
            coh_path = r'.\Coherence.exe'
        
        self.init(coh_path)
        
        try:
            self.app = Application(backend="uia").connect(path=self.coh_exe, pid=pid)
            self.wtop = self.app.top_window()
        except Exception as e:
            RAISE(f"Hang Error: {str(e)}")

        #print(f'app {app}')
        #print(f'wtop {wtop}')
        self.placeholder()

    def select_ribbon(self, ribb):
        rib_sel = uw.get_child_chk(self.rib_tab, name=ribb, ctrl_type='TabItem')
        uw.win_click(rib_sel)
        toolbar = uw.get_child_chk(self.rib_grp, name=ribb, ctrl_type='ToolBar')
        print(f'toolbar {toolbar}')
        return toolbar

    def select_ribbon_butt(self, ribb, butt):
        toolbar = self.select_ribbon(ribb)
        print(f'toolbar {toolbar}')
        bt = uw.get_child_chk(toolbar, name=butt, ctrl_type='Button', deep=2)
        return bt

    def click_ribbon_butt(self, ribb, butt, wait_end=1): 
        bt = self.select_ribbon_butt(ribb, butt)
        uw.win_click(bt)
        sleep(wait_end)
        return bt

    def ready(self):
        return self.app != None and self.wtop != None and self.rib_tab != None and self.rib_grp != None and self.st_bar != None

    def reload(self, wait_init=1, wait_in=1, wait_end=1, timeout=5):        
        now = datetime.now() 
        sleep(wait_init)
        done = 0
        while (1):
            try:
                self.wtop = self.app.top_window()
                if self.app and self.wtop and not re.match('Starting Coherence.*', self.wtop.window_text()):
                    done = 1
                    sleep(0.5)
                    break
            except Exception as e:
                break
            elaps = (datetime.now()-now).seconds
            if (elaps>timeout):
                break
            sleep(wait_in)
        if done:
            sleep(wait_end)
            self.placeholder()
        VERIFY(self.ready(), "Connection Was not Ready by Timeout")

    def wait_conn_ready(self, to_sec=30, to_err_sec=5, delay=1, wait_init=0.5, wait_end=0.5):
        now = datetime.now() 
        sleep(wait_init)
        done = 0
        print ('Wait Connection Ready...')
        while (1):
            elaps = (datetime.now()-now).seconds
            if elaps>to_sec:
                    break
            cld = uw.get_child_chk(self.st_bar, 'Ready', ctrl_type='Text', verify=False)
            if cld:
                done = 1
                break
            if elaps > to_err_sec:
                cld = uw.get_child_chk(self.st_bar, 'Failed', ctrl_type='Text', verify=False)
            if cld:
                done = 0
                break
            sleep(delay)
        if done:
            sleep(wait_end)
        utl.play_sound('success' if done else 'fail')
        return done==1

env = AppEnv()              # class singleton
#endregion


##########################################################
# Others

def sleep(sec):
    opt_speed = config.get('opt.speed')
    if opt_speed:
        speed = float(opt_speed)/100  
    else:
        speed=1
    
    time.sleep(sec/speed)


if __name__ == '__main__':
    test_config.load(r'.\utils\test\test_cd_rfq.json')
    print(config('coh.addin'))