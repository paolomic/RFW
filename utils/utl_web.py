
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


##########################################################
#region - Web Application - Browser 

def look_for_username_control():
    main = uw.get_main_wnd('CanDeal Evolution.*Google Chrome.*', use_re=1)  
    if main:
        edit = uw.get_child(wapp.doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1, deep=2)
        if edit:
            return True
    return None

wait_reload_login =  utl.retry_fun(retry_timeout=15, retry_delay=1, wait_init=0.25, wait_end=0.25)(look_for_username_control)


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

    def launch_url(self, url=None, wait_end=0.5):
        if url:            
            self.url = url
        subprocess.run(["start", "chrome", "--new-window", self.url], shell=True)
        #utl.play_sound('success')
        
        #complete reload - waiting for username control
        wait_reload_login()
        
        self.hang_main(retry_timeout=15)
        uw.win_maximize(self.main, maximize=False)
        uw.win_move(self.main, 950, 0)
        uw.win_resize(self.main, 1000, 1080)

        uw.sleep(wait_end)


    #@utl.chrono
    def hang_main(self, url=None, wait_end=1, retry_timeout=0):
        if url:
            self.init(url)
        main = uw.get_main_wnd_retry('CanDeal Evolution.*Google Chrome.*', use_re=1, retry_timeout=retry_timeout)  
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
        if evt=='terminate'  or conn=='terminate':
            print('Terminate: Web App Browsers')
            to = utl.TimeOut(10)
            while not to.expired():
                main = uw.get_main_wnd('CanDeal Evolution - Google Chrome.*', use_re=1)
                if main:
                    uw.win_close(main)
                    #utl.process_kill(main)         # forced closure, ma chiude TUTTI i chrome - hanno lo stesso pid ?
                else:
                    break
            uw.sleep(1)
        elif evt=='start':
            pass
        elif evt=='exit':
            pass
        
    def hang_rfq(self, url=None, move=True):
        pass

    def close_app(self, url=None):
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
        edit = uw.get_child_retry(self.doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1, retry_timeout=15)
        uw.edit_set(edit, config.get('web.user'))
        edit = uw.get_child_chk(self.doc, name='PASSWORD.', automation_id='password', ctrl_type='Edit', use_re=1)
        uw.edit_set(edit, config.get('web.pass'))
        keyboard.press_and_release('esc')
        butt = uw.get_child_chk(self.doc, name='LOGIN.*', ctrl_type='Button', use_re=1)
        uw.win_click(butt)
        uw.sleep(3)                  

        to = utl.TimeOut(60)            # smartwait check hang
        while  not to.expired():
            try:
                #wrn = uw.get_child_retry(self.doc, name='Notifications popup are disabled', retry_timeout=15)
                wrn = uw.get_child(self.doc, name='Notifications popup are disabled')
                if wrn:
                    butt = uw.get_child_chk(wrn, name='OK', deep=2)
                    uw.win_click(butt)
                
                wapp.hang_main()
                butt = uw.get_child_chk(self.doc, name='', deep=2)      
                if butt:
                    break
            except:
                pass

    def filter_clear(self):
       butt = uw.get_child_chk(self.doc, name='', deep=2)              # clear - todo AutomationId
       uw.win_click(butt, wait_end=.6)

    def filter_set_security(self, sec):
        combo = uw.get_child_retry(self.doc, name='Search Security', ctrl_type='ComboBox', deep=2, retry_timeout=10)  # clear - todo AutomationId
        uw.edit_set(combo, sec, wait_end=2)                                     # crtitico a volte non abilita
        keyboard.press_and_release('enter')
        butt = uw.get_child_retry(self.doc, name='', deep=2, retry_timeout=10)        # retry: long timeout web
        uw.win_click(butt, wait_end=1)

    def new_rfq(self):
        butt = uw.get_child_retry(self.doc, name='NEW RFQ', ctrl_type='Button', deep=3, retry_timeout=15, recover_fun=wapp.hang_main)  # retry: long timeout web - # todo - smart wait
        uw.win_click(butt, wait_end=.6)

wapp = WebAppEnv()              # class singleton

#endregion

##########################################################
#region - WebTable 

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

#endregion
if __name__ == '__main__':
    #wapp.hang_main(url=None, wait_end=1, retry_timeout=15)
    wait_reload_login()