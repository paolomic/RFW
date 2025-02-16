import time
from pywinauto import Application
import subprocess
from pathlib import Path
import re
import os
from datetime import datetime, timedelta
import keyboard

import utl_win as uw
import utl  as utl

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


    # Starting....
    def reset_wsp(self):
        path_wsp = Path(config.get('coh.wsp'))
        if path_wsp.exists():
            print('Remove Workspace...')
            path_wsp.unlink()
            VERIFY(not path_wsp.exists(), 'Wsp Exist')
        #path_wsp_folder = Path(config.get('coh.wsp').replace('.wsp4', '.wsp4_wrk'))
        #if (path_wsp_folder.exists()):
        #    path_wsp_folder.rmdir()
        #VERIFY(not path_wsp_folder.exists(), 'Wsp Folder Exist')

    def start_dialog(self, wsp, addins):
        edit = uw.get_child_chk(app.wtop, automation_id='12429', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, wsp)

        list = uw.get_child_chk(app.wtop, name='Import From', ctrl_type='List', deep=3)
        uw.list_check(list, '*', False)
        uw.list_check(list, addins, True)

        butt = uw.get_child_chk(app.wtop, automation_id='1', ctrl_type='Button', deep=3)
        if not config.get('opt.reuse_wsp')=='yes':
            VERIFY(butt.window_text()=='Create', 'Can`t Create New Workspace')

        uw.win_click(butt, wait_end=0.5)
        uw.warning_replay('This workspace has not been closed properly', 'No')

    # After Start
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

    def connection(self, start=True, addins = []):
        if start:
            if config.get('opt.close_all_pages')=='yes':
                uw.page_close_all()
            
            addins = ['MetaMarket']                                                     # TODO pass form Robot ?
            for addin in addins:
                butt = app.select_ribbon_butt(addin, 'Auto Connect')
                if not uw.butt_is_checked(butt):
                    uw.win_click(butt)

            butt = app.select_ribbon_butt('Home', 'Auto Connect')
            if not uw.butt_is_checked(butt):
                uw.win_click(butt)

            if app.wait_conn_ready(to_sec=120, to_err_sec=5, delay=2):
                print ('Connection Ready')
            else:
                RAISE("Connection Fail")
        else:
            butt = app.select_ribbon_butt('Home', 'Auto Connect')
            if uw.butt_is_checked(butt):
                uw.win_click(butt)
                uw.warning_replay('Do you want to disable Auto Connect mode and stop all connections?', 'OK')


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

    def manage_conn(self, evt, conn):
        op = utl.get_conn_events(conn, 'coh')
        if not op:
            return
        if evt=='start':
            if 'new' in op:
                app.launch_app(config.get('coh.path'))
            elif 'hang' in op:
                app.hang_app(config.get('coh.path'))
                app.wtop.set_focus()

            if 'new' in op or 'hang' in op:
                VERIFY(app.app and app.wtop, "Hang or New Session Failed")
        if evt=='exit':
            if 'kill' in op:
                uw.session_close(app.wtop, wait_init=1, wait_end=1, logoff=True)
                exist = 0
                try:
                    app.hang_app(config.get('coh.path'))
                    exist=1
                except Exception as e:
                    pass
                VERIFY(not exist, 'Close Session Failed. Process still Exists')
        if evt=='timeout':
            print('Timeout: kill Coherence instance')
            utl.process_kill(self.wtop)
            #print(f'Forcing Closure Window {self.wtop.handle}')
            #uw.win_close(self.wtop)
            #uw.session_close(self.wtop, wait_init=1, wait_end=1, logoff=True)

class Settings:
    #private
    pane = None
    list = None

    def open(self):
        butt = uw.get_child_chk(app.wtop, name='Settings', ctrl_type='Button', deep=4)          # Settings gia aperto se New Wsp
        uw.win_click(butt)

        self.pane = uw.get_child_chk(app.wtop, name='Settings', ctrl_type='Pane', deep=3)
        self.list = uw.get_child_chk(self.pane, automation_id='103', ctrl_type='List', deep=3)

    def close(self):
        butt = uw.get_child_chk(self.pane, name='OK', ctrl_type='Button', deep=3)
        uw.win_click(butt)
    
    def set_platform(self, host, port, user, passwd, save_bw):
        edit = uw.get_child_chk(self.pane, name='Host', ctrl_type='Edit', deep=1)
        uw.edit_set(edit, host)
        edit = uw.get_child_chk(self.pane, name='Port', ctrl_type='Edit', deep=1)
        uw.edit_set(edit, port)
        edit = uw.get_child_chk(self.pane, name='User name', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, user)
        edit = uw.get_child_chk(self.pane, automation_id='11303', ctrl_type='Edit', deep=3)
        uw.edit_set(edit, passwd)
        
        if save_bw:
            butt = uw.get_child_chk(self.pane, name='Bandwidth Saving', ctrl_type='CheckBox', deep=3)
            if not uw.butt_is_checked(butt):
                uw.win_click(butt)

    def metamarket(self, trace_lev):
        uw.list_select(self.list, "MetaMarket")
        trace = uw.get_child_chk(self.pane, name='Trace Level', ctrl_type='Custom', deep=3)
        uw.win_click(trace, mode='combo')
        #sleep(.25)
        #ud.dump_uia_tree(env.wtop)         # non c'e' lista popup
        uw.hide_select(-1)                  # Todo Control Inside
        keyboard.press("enter")             # Confirm Selection
        sleep(.25)

    def workspace(self, trace_lev):
        uw.list_select(self.list, "Workspace")
        combo = uw.get_child_chk(self.pane, automation_id='11347', ctrl_type='ComboBox', deep=3)         # Todo: Input Per Valore
        uw.win_click(combo)
        keyboard.press("end")
        keyboard.press("enter")
        combo = uw.get_child_chk(self.pane, automation_id='11345', ctrl_type='ComboBox', deep=3)
        uw.win_click(combo)
        keyboard.press("end")
        keyboard.press("enter")

class BondDlg:
    #private
    dlg = None

    def __init__(self, rfqid=''):
        self.dlg_rfq = uw.get_child_chk(app.wtop, name=r"RFQ Outright \[CANDEAL\/BOND\] \[\d+\]", ctrl_type='Pane', deep=1, use_re=1)  
   
    def press(self, but_name):
        butt = uw.get_child_chk(self.dlg_rfq, name=but_name, ctrl_type='Button', deep=1)  
        uw.win_click(butt)

app = AppEnv()              # class singleton
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