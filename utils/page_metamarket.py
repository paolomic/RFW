import keyboard
import mouse

import utl_win as uw
from utl_win import sleep
from utl_app import app
import utl_log as ul

import utl  as utl

from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud
from utl_config import config


class PageSecurityBrowser:
    #private
    wnd = None
    grid = None

    def __init__(self, new=False):
        if new:
            self.open()
        else:
            self.filteruse()
        pass

    def open(self):
        app.click_ribbon_butt('Trading', 'Security Browser')
        self.use()
        uw.win_resize(self.wnd, 1400, 450)

    def use(self):
        self.wnd = uw.get_child_chk(app.wtop, name='Security Browser.*', ctrl_type='Pane', use_re=True, deep=1)
        self.grid = uw.page_get_grid(self.wnd)

    def filter(self, key):
        search_edit = uw.get_child_chk(self.wnd, name='Reference:', ctrl_type='Edit', deep=10)     # reset search 
        search_butt = uw.get_child_chk(self.wnd, name='Search', ctrl_type='Button', deep=10)
        uw.edit_set(search_edit, key)
        uw.win_click(search_butt, wait_end=.5)

    def tree_filter(self, exc, mrk):
        treekey = f'{exc} - {mrk}'
        item = uw.get_child_chk(self.wnd, name=treekey, ctrl_type='TreeItem', deep=10) 
        uw.win_click(item)

class PageOrders:
    #private
    wnd = None
    grid = None

    def __init__(self, new=False):
        if new:
            self.open()
        else:
            self.filteruse()
        pass

    def open(self):
        app.click_ribbon_butt('Trading', 'Orders')
        self.use()
        uw.win_resize(self.wnd, 1400, 450)

    def use(self):
        self.wnd = uw.get_child_chk(app.wtop, name='Orders.*', ctrl_type='Pane', use_re=1, deep=2)
        self.grid = uw.page_get_grid(self.wnd)

    def set_filter(self, name, key):
        edit = uw.get_child_chk(self.wnd, name=name, ctrl_type='Edit', deep=5)  
        uw.edit_set(edit, key)

    def clear_filter(self):
         butt = uw.get_child_chk(self.wnd, name='Clear Filter', ctrl_type='Button', deep=5)  
         uw.win_click(butt)

    def apply_filter(self):
         butt = uw.get_child_chk(self.wnd, name='Apply', ctrl_type='Button', deep=5)  
         uw.win_click(butt)



class DlgNewCareOrder:
    #private
    wnd = None
    adv_wnd = None

    def __init__(self):
        self.wnd = uw.get_child_chk(app.wtop, name="New Care Order.*", ctrl_type="Pane", use_re=1)
        uw.win_move(self.wnd, 333,333)                              # davanti alla toolbar sembra creare problemi a step successivo
        self.wnd.set_focus()

    def advanced(self, open=True):
        adv = uw.get_child_chk(self.wnd, automation_id='13652', ctrl_type="CheckBox", use_re=1)
        if open:
            if not uw.butt_is_checked(adv):
                uw.win_click(adv)
        else:
            if uw.butt_is_checked(adv):
                uw.win_click(adv)
        self.adv_wnd = uw.get_child(self.wnd, name="Order Advanced Parameters", ctrl_type="Pane")
                
    def set_qty(self, qty):
        edit = uw.get_child_chk(self.wnd, automation_id='12216')  
        uw.edit_set(edit, qty)

    def set_price(self, prc):
        edit = uw.get_child_chk(self.wnd, automation_id='12214')  
        uw.edit_set(edit, prc)
    
    def set_alias(self, alias):
        edit = uw.get_child_chk(self.wnd, automation_id='12796')     # Alias
        uw.win_click(edit)
        keyboard.write(alias)                               # popup is hide - or edit_set
        keyboard.press("tab")

    def set_note(self, note):
        edit = uw.get_child_chk(self.adv_wnd, automation_id='12954')  
        uw.edit_set(edit, note)

    def send(self):
        but = uw.get_child_chk(self.wnd, automation_id='1')          # Buy     
        uw.win_click(but)

    def retrieve_orderid(self, mytag, send_time):
        log_path = uw.get_log_path(config.get('coh.wsp'), 'MetaMarket')
        return ul.GetLogRows(log_path, 'CLIENT_ORDER', 'ComplianceText', mytag, send_time, retry = 10, wait_s = 1)

    def close(self):
        uw.win_close(self.wnd)     