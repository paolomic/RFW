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

    @utl.chrono_function
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

    @utl.chrono_function
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
#ewgion - Web Environment 

class WebAppEnv:
    #private
    url = None

    def reset(self):
        self.url = None

    #@utl.chrono_function
    def placeholder(self):
        pass

    def init(self, url): 
        self.reset()
        self.url = url

    def launch_url(self, url=None, wait_end=3):
        if url:
            self.init(url)        
        subprocess.run(["start", "chrome", "--new-window", self.url], shell=True)
        utl.play_sound('success')
        uw.sleep(wait_end)
        return self.hang_main()

    #@utl.chrono_function
    def hang_main(self, url=None, wait_end=1):
        if url:
            self.init(url)
        brw = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)  
        print(f'brw:{brw}')
        VERIFY(brw, 'browser start fail')
        try:
            #ud.dump_uia_tree(brw, max_depth=1)                         # patch 
            doc = uw.get_child_chk(brw, name='CanDeal Evolution', ctrl_type='Document')   # main page
            print(f'doc:{doc} logged')
        except:
            ud.dump_uia_tree(brw, max_depth=3)                      # PATCH - MISTERO atrimenti non trova il doc
            doc = uw.get_child_chk(brw, ctrl_type='Document')       # login page
            print(f'doc:{doc} loggin')
        try:
            pass
            # todo verifica unicita
        except Exception as e:
            RAISE(f"Start Error: {str(e)}")
        
        uw.sleep(wait_end)
        return (brw, doc)

    def hang_rfq(self, url=None):
        uw.sleep(0.25)
        rfq = uw.get_main_wnd('New Bond RFQ.*Google Chrome.*', use_re=1)
        VERIFY(rfq, 'rfq panel fail')
        table = uw.get_child_chk(rfq, ctrl_type='Table', deep=2)
        grp = uw.get_child_chk(table, ctrl_type='Group', deep=1)        # group combo type
        uw.sleep(0.25)

        return (rfq, table, grp)

    def kill_app(self, url=None):
        while 1:
            inst = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)  
            if not inst:
                return
            uw.win_close(inst)

    def get_doc(self):
        return 

    #todo metterla in modulo opportuno
    # todo - heade e row potrebbero forse non essere calcolati tutte le volte
    def get_answer(self, table):
        users=[]
        
        try:
            table2 = uw.get_child(table, ctrl_type='Table')
            header = uw.get_child(table, ctrl_type='Custom')    #'Dealer Good For Qty Yield Price Ref Sprd.*'
            rows = uw.get_child(table2, ctrl_type='Group')

            for row in rows.children():
                cols =  row.children()
                col_user = cols[0]
                user =cols[0].children()[1]
                qty =cols[2].children()[2]
                prc =cols[3].children()[2]
                if (len(user.window_text())>2):    
                    users.append((user.window_text(), qty.window_text(), prc.window_text()))
        except:
            pass
        
        return users

    class WebTable:                                                    # todo to move in utl_web
        header = []
        rows = []

        def node_str(self, node):
            res = ''
            for item in node.children():
                res += item.window_text()

        def reset(self):
            self.header = []
            self.rows = []

        def load(self, table, reload_header=False, nrow=0):             # todo limitare row, col ?
            if len(self.header==0) or reload_header:
                self.header = []
                hd = uw.get_child(table, ctrl_type='Custom') 
                for colh in hd.children():
                    col_name = self.node_str(colh)
                    self.header.append(col_name)
            table2 = uw.get_child(table, ctrl_type='Table')
            rows = uw.get_child(table2, ctrl_type='Group')  
            for row in rows.children():
                data_row = []
                cells =  row.children()
                for cell in cells:
                    data_row.append(self.node_str(cell))
                self.rows.append(data_row)



wenv = WebAppEnv()              # class singleton




#endregion

##########################################################
# App Options

class AppOptions:
    opt = None
    def set(self, options):
        self.opt = options
    def get(self, key):
        try:
            find_val = self.opt[key]
            return find_val
        except Exception as e:
            return None
         
opt = AppOptions()


##########################################################
# Others

def sleep(sec):
    opt_speed = opt.get('speed')
    if opt_speed:
        speed = float(eval(opt_speed))/100  
    else:
        speed=1
    
    time.sleep(sec/speed)


if __name__ == '__main__':
    def fun1():
        print(3/0)

    def fun2():
        fun1()

    def fun3():
        fun2()

    try:
        fun3()
    except Exception as e:
        DUMP( str(e))