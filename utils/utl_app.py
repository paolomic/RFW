import time
from pywinauto import Application
import os

import utl_win as uw
from utl_win import sleep, VERIFY, RAISE

class AppEnv:
    app = None
    wtop = None
    rib_tab = None
    rib_grp = None
    st_bar = None

    #private
    coh_path = None
    coh_exe = None

    def reset(self):
        self.app = None
        self.wtop = None
        self.rib_tab = None
        self.rib_grp = None
        self.st_bar = None
        
        #private
        coh_path = None
        coh_exe = None

    def set(self, app):
        self.reset()
        
        self.app = app
        try:
            self.wtop = app.top_window()
        except:
            pass
        try:
            self.rib_tab = uw.get_child_chk(self.wtop, name='Ribbon Tabs', ctrl_type='Group', deep=3, verify=False)      # TODO verify condizionale a wtop
        except:
            pass
        try:
            self.rib_grp = uw.get_child_chk(self.wtop, automation_id='59398', ctrl_type='ToolBar', deep=3, verify=False)
        except:
            pass
        try:
            self.st_bar = uw.get_child_chk(self.wtop, name='StatusBar', ctrl_type='StatusBar', verify=False)
        except:
            pass
        #print (self)

    def init(self, coh_path): 
        self.reset()
        self.coh_path = coh_path
        self.coh_exe = os.path.basename(coh_path)

    def launch_app(self, coh_path, unique=True):
        self.init(coh_path)
        exe_name = os.path.basename(self.coh_path)

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
            app = Application(backend="uia").start(self.coh_path)
            time.sleep(1)                                               # TODO attesa attiva
            wtop = app.top_window()
        except Exception as e:
            RAISE(f"Start Error: {str(e)}")
            
        #print(f'app {app}')
        #print(f'wtop {wtop}')
        self.set(app)

    def hang_app(self, coh_path):
        self.init(coh_path)
        hang_ok = 0
        self.reset()
        exe_name = os.path.basename(self.coh_path)
        
        try:
            app = Application(backend="uia").connect(path=self.coh_exe)
            wtop = app.top_window()
            hang_ok = 1
        except Exception as e:
            RAISE(f"Hang Error: {str(e)}")

        print(f'app {app}')
        print(f'wtop {wtop}')
        self.set(app)

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


    def reload(self):         # mode= hang / launch  / hang_or_launch 
        self.hang_app(self.coh_path)

env = AppEnv()              # session singleton
