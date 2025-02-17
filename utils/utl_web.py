
import time
from pywinauto import Application
import subprocess
import keyboard

import utl_win as uw
import utl  as utl

import re
import os
from datetime import datetime, timedelta

from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud

from utl_config import config

class WebAppEnv:
    #private
    url = None
    main = None
    doc = None

    def reset(self):
        self.url = None

    def init(self, url): 
        if url:            
            self.url = url

    def launch_url(self, url=None, wait_end=3):
        if url:            
            self.url = url
        subprocess.run(["start", "chrome", "--new-window", self.url], shell=True)
        utl.play_sound('success')
        uw.sleep(wait_end)
        self.hang_main()
        uw.win_maximize(self.main, maximize=False)
        uw.win_move(self.main, 950, 0)
        uw.win_resize(self.main, 1000, 1080)

    #@utl.chrono
    def hang_main(self, url=None, wait_end=1):
        if url:
            self.init(url)
        main = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)  
        #@print(f'brw:{brw}')                                      # very long string     
        VERIFY(main, 'browser start fail')
        try:
            #ud.dump_uia_tree(brw, max_depth=1)                
            doc = uw.get_child_chk(main, name='CanDeal Evolution', ctrl_type='Document')   # main page
            #print(f'doc:{doc}')
        except:
            ud.dump_uia_tree(main, max_depth=3)                      # PATCH - MISTERO atrimenti non trova il doc
            doc = uw.get_child_chk(main, ctrl_type='Document')       # login page
            #print(f'doc:{doc}')
        try:
            pass
            # todo verifica unicita
        except Exception as e:
            RAISE(f"Start Error: {str(e)}")
        
        uw.sleep(wait_end)

        self.main = main
        self.doc = doc

    def manage_conn(self, evt, conn):
        if evt=='terminate':
            print('Terminate: Web App Browsers')
            to = utl.TimeOut(10)
            while not to.expired():
                main = uw.get_main_wnd('CanDeal Evolution - Google Chrome.*', use_re=1)
                if main:
                    uw.win_close(main)
                    #utl.process_kill(main)         # forced closure, ma chiude TUTTI i chrome - hanno lo stesso pid ?
                    uw.sleep(2)
                else:
                    break
        elif evt=='start':
            pass
        elif evt=='exit':
            pass
        
            
    def hang_rfq(self, url=None, move=True):
        pass

    def kill_app(self, url=None):
        while 1:
            inst = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)  
            if not inst:
                return
            uw.win_close(inst)

    def get_main(self):
        return self.main

    def get_doc(self):  
        return self.doc
    
    def set_login_user_password(self):
        edit = uw.get_child_chk(wapp.doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1)
        uw.edit_set(edit, config.get('web.user'))
        edit = uw.get_child_chk(wapp.doc, name='PASSWORD.', automation_id='password', ctrl_type='Edit', use_re=1)
        uw.edit_set(edit, config.get('web.pass'))
        keyboard.press_and_release('esc')
        butt = uw.get_child_chk(wapp.doc, name='LOGIN.*', ctrl_type='Button', use_re=1)
        uw.win_click(butt)
        uw.sleep(2)                   # todo - smart wait
        try:
            wrn = uw.get_child_chk(wapp.doc, name='Notifications popup are disabled')
            butt = uw.get_child_chk(wrn, name='OK', deep=2)
            uw.win_click(butt)
        except:
            pass

    def filter_clear(self):
       butt = uw.get_child_chk(wapp.doc, name='', deep=2)              # clear - todo AutomationId
       uw.win_click(butt, wait_end=.5)

    def filter_set_security(self, sec):
        combo = uw.get_child_chk(wapp.doc, name='Search Security', ctrl_type='ComboBox', deep=2)  # clear - todo AutomationId
        uw.edit_set(combo, sec, wait_end=.5)
        butt = uw.get_child_retry(wapp.doc, name='', deep=2, timeout=4)        # retry: long timeout web
        uw.win_click(butt, wait_end=.5)

    def new_rfq(self):
        butt = uw.get_child_retry(wapp.doc, name='NEW RFQ', ctrl_type='Button', deep=2, timeout=4)  # retry: long timeout web
        uw.win_click(butt, wait_end=.5)

wapp = WebAppEnv()              # class singleton


class WebTable:
    def __init__(self, table=None, load=False):
        self.header = []  # Lista per memorizzare gli header della tabella
        self.rows = []    # Lista di dizionari per memorizzare le righe della tabella
        self.table = table
        if load and self.table:
            self.load(self.table)

    def reset(self):
        self.header = []
        self.rows = []

    def node_str(self, node):
        res = ''
        for item in node.children():
            res += item.window_text()
        return res.strip()  # Rimuove spazi bianchi in eccesso

    #@utl.chrono
    def load(self, table=None, reload_header=False, nrow=0):
        if table:
            self.table = table

        # Carica l'header se necessario
        if len(self.header) == 0 or reload_header:
            hd = uw.get_child(self.table, ctrl_type='Custom')  # Assicurati che 'Custom' sia corretto
            if hd:
                for colh in hd.children():
                    col_name = colh.window_text()
                    self.header.append(col_name)
        self.rows = []
        data_node = uw.get_child(self.table, ctrl_type='Group')  # Assicurati che 'Group' sia corretto
        if data_node:
            row_count = 0
            for row_node in data_node.children():
                data_row = {}
                cells = row_node.children()
                for i, cell in enumerate(cells):
                    if i < len(self.header):  # Assicurati di non superare il numero di colonne
                        data_row[self.header[i]] = self.node_str(cell)
                self.rows.append(data_row)
                row_count += 1
                if nrow > 0 and row_count >= nrow:  # Interrompi se è stato raggiunto il numero massimo di righe
                    break
        return self.rows


class WebBondDlg:
    main = NotImplementedError
    table = None
    tag_time = None
    tag_state = None
    grid:WebTable = None
    timeout:utl.TimeOut = None

    def __init__(self, timeout = 240, move=True):
        uw.sleep(0.25)
        self.main = uw.get_main_wnd('New Bond RFQ.*Google Chrome.*', use_re=1)
        VERIFY(self.main, 'rfq panel fail')
        if move:
            uw.win_move(self.main, 1300, 500)
        self.table = uw.get_child_chk(self.main, ctrl_type='Table', deep=2)
        #print(ud.dump_uia_tree(self.table))
        uw.sleep(0.25)
        self.timeout = utl.TimeOut(timeout)

    # Before Send - Prepare Rfq
    def set_combo(self, rfq_type):
        combo = uw.get_child_retry(self.table, name='-', ctrl_type='ComboBox', deep=2)   # mancano locator
        uw.win_click(combo)
        uw.edit_set(combo, rfq_type)

    def set_price(self, price):
        label = uw.get_child_retry(self.table, name='PRICE', ctrl_type='Text')
        combo = uw.get_child_after(label, ctrl_type='Spinner')                  # todo mancano Key
        uw.edit_set_manual(combo, price, reset=1)               # usa keyboard

    def set_qty(self, qty):
        label = uw.get_child_chk(self.table, name='QTY', ctrl_type='Text')
        combo = uw.get_child_after(label, ctrl_type='Spinner')
        uw.edit_set_manual(combo, qty, reset=1)             # usa keyboard
 
    def set_dealer(self, delaer):
        butt = uw.get_child_chk(self.table, name=delaer, ctrl_type='Button')
        uw.win_click(butt)

    def send(self):
        butt = uw.get_child_chk(self.table, name='SEND', ctrl_type='Button')
        uw.win_click(butt)

    # After Send - Manage Rfq

    def prepare_grid(self):
        if not self.grid:
            self.grid = WebTable(uw.get_child_chk(self.table, ctrl_type='Table'))

    def get_time(self):
        try:
            if not self.tag_time:
                self.tag_time = uw.get_child(self.table, name=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$', use_re=1, deep=6)         # todo - sepolto senza locator
            txt_time = self.tag_time.window_text()
        except:
            self.tag_time = None
            return None
        if not self.tag_time or not txt_time:
            return None
        return txt_time

    def get_final_state(self):
        try:
            self.tag_state = uw.get_child(self.table, name='.*(ENDED|EXPIRED|DONE).*', use_re=1)                # todo - ottimizzare se' e' lo stesso del time ?
            return self.tag_state.window_text()
        except:
            return None

    def is_live(self):
        if self.timeout.expired():                  # time protection
            return False
        return self.get_time() != None                # or return self.get_final_state == None 
        
    def get_short_answer(self):        # short fast version for load - serve?
        self.prepare_grid()       
        users=[]
        try:
            header = uw.get_child(self.grid.table, ctrl_type='Custom')    #'Dealer Good For Qty Yield Price Ref Sprd.*'
            rows = uw.get_child(self.grid.table, ctrl_type='Group')

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

    def get_answer(self, short=False):
        self.prepare_grid()
        if short:
            return self.get_short_answer()
        else:
            return self.grid.load()



""" 
Esempio Table Bond Dlg:
Table: 
    Custom - contiene Header, 
    Group - contiene 1 row
    Group - contiene 1 row
    ...

Level 0: Table (Class: , AutomationId: ), Visible=True, Text=None, Texts=[['Dealer Good For Qty Yield Price Ref Sprd W/O Call Date Status Settl Date Maturity'], ['']]
    ├── Level 1: Custom (Class: , AutomationId: ), Visible=True, Text='Dealer Good For Qty Yield Price Ref Sprd W/O Call Date Status Settl Date Maturity', Texts=['Dealer Good For Qty Yield Price Ref Sprd W/O Call Date Status Settl Date Maturity']
        ├── Level 2: Header (Class: , AutomationId: ), Visible=True, Text='Dealer', Texts=['Dealer']
        ├── Level 2: Header (Class: , AutomationId: ), Visible=True, Text='Good For', Texts=['Good For']
        ├── Level 2: Header (Class: , AutomationId: ), Visible=True, Text='Qty', Texts=['Qty']
        ...
    ├── Level 1: Group (Class: , AutomationId: ), Visible=True, Text=None, Texts=['']                   # Row.1
        ├── Level 2: Custom (Class: , AutomationId: ), Visible=True, Text=None, Texts=['']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ', 'RBC']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='RBC', Texts=['RBC']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ', '  ', '-']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='-', Texts=['-']
    ├── Level 1: Group (Class: , AutomationId: ), Visible=True, Text=None, Texts=['']                   # Row.2
        ├── Level 2: Custom (Class: , AutomationId: ), Visible=True, Text=None, Texts=['']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ', 'RBC']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='RBC', Texts=['RBC']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
            ├── Level 3: DataItem (Class: , AutomationId: ), Visible=True, Text=None, Texts=['  ', '  ', '-']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=False, Text='  ', Texts=['  ']
                ├── Level 4: Text (Class: , AutomationId: ), Visible=True, Text='-', Texts=['-']
 """