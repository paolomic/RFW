import keyboard
import mouse

import utl_win as uw
from utl_win import sleep
from utl_app import app

import utl  as utl

from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud
from utl_config import config



class PageSettings:
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
        edit = uw.get_child_chk(self.pane, name=r'[Primary|Host]', ctrl_type='Edit', deep=1, use_re=1)
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

