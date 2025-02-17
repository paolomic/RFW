import time
from pywinauto import Application
import subprocess
import keyboard

import utl_win as uw
from utl_web import wapp, WebTable
import utl  as utl

import re
import os
from datetime import datetime, timedelta

from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud

from utl_config import config


class WebDlgRfqBond:
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