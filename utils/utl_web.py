
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



class WebAppEnv:
    #private
    url = None

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

    #@utl.chrono
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


webapp = WebAppEnv()              # class singleton

class WebTable:
    def __init__(self, table=None, load=True):
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

    @utl.chrono
    def load(self, table=None, reload_header=False, nrow=0):
        if table:
            self.table = table

        self.reset()  # Resetta la tabella prima di caricare nuovi dati

        # Carica l'header se necessario
        if len(self.header) == 0 or reload_header:
            hd = uw.get_child(self.table, ctrl_type='Custom')  # Assicurati che 'Custom' sia corretto
            if hd:
                for colh in hd.children():
                    col_name = colh.window_text()
                    self.header.append(col_name)

        rows = uw.get_child(self.table, ctrl_type='Group')  # Assicurati che 'Group' sia corretto
        if rows:
            row_count = 0
            for row in rows.children():
                data_row = {}
                cells = row.children()
                for i, cell in enumerate(cells):
                    if i < len(self.header):  # Assicurati di non superare il numero di colonne
                        data_row[self.header[i]] = self.node_str(cell)
                self.rows.append(data_row)
                row_count += 1
                if nrow > 0 and row_count >= nrow:  # Interrompi se è stato raggiunto il numero massimo di righe
                    break

    def get_answer(self, table=None):        # short fast version for load - serve?
        if table:
            self.table = table
        
        users=[]
        
        try:
            header = uw.get_child(self.table, ctrl_type='Custom')    #'Dealer Good For Qty Yield Price Ref Sprd.*'
            rows = uw.get_child(self.table, ctrl_type='Group')

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


