import time
from pywinauto import Application
import os

import utl_win as uw
from utl_win import VERIFY, RAISE

class AppEnv:
    app = None
    wtop = None
    rib_tab = None
    rib_grp = None
    st_bar = None

    #private
    coh_path = None
    coh_exe = None
    coh_title = None

    def reset(self):
        self.app = None
        self.wtop = None
        self.rib_tab = None
        self.rib_grp = None
        self.st_bar = None
        
        #private
        coh_path = None
        coh_exe = None
        coh_title = None

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

    def init(self, coh_path, coh_title): 
        self.reset()
        self.coh_path = coh_path
        self.coh_title = coh_title
        self.coh_exe = os.path.basename(coh_path)

    def launch_app(self, coh_path, coh_title):
        self.init(coh_path, coh_title)
        exe_name = os.path.basename(self.coh_path)

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

    def hang_app(self, coh_path, coh_title):
        self.init(coh_path, coh_title)
        hang_ok = 0
        self.reset()
        exe_name = os.path.basename(self.coh_path)
        
        try:
            app = Application(backend="uia").connect(path=self.coh_exe, title=self.coh_title)
            wtop = app.top_window()
            hang_ok = 1
        except Exception as e:
            RAISE(f"Hang Error: {str(e)}")

        print(f'app {app}')
        print(f'wtop {wtop}')
        self.set(app)

    def hang_app_2(self, mode='hang_or_launch'):         # mode= hang / launch  / hang_or_launch 
        hang_ok = 0
        self.reset()
        exe_name = os.path.basename(self.coh_path)
        if (mode=='hang' or mode=='hang_or_launch'):
            try:
                app = Application(backend="uia").connect(path=self.coh_exe, title=self.coh_title)
                wtop = app.top_window()
                hang_ok = 1
            except Exception:
                pass

            if ((not hang_ok and mode=='hang_or_launch') or mode=='launch '):
                try:
                    print('Starting new instance...')
                    app = Application(backend="uia").start(self.coh_path)
                    time.sleep(1)  # Attende che l'app si avvii completamente
                    wtop = app.top_window()
                except Exception as e:
                    print(f"Start Error: {str(e)}")
                    raise
            
            if not wtop:
                raise Exception("Open Error")
            
            print(f'app {app}')
            print(f'wtop {wtop}')
        self.set(app)

    def reload(self):         # mode= hang / launch  / hang_or_launch 
        self.hang_app(self.coh_path, self.coh_title)

env = AppEnv()              # session singleton
