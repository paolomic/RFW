import keyboard
import mouse

import utl_win as uw
from utl_win import sleep
from utl_app import app

import utl  as utl

from utl_verifier import VERIFY, RAISE, DUMP
import utl_dump as ud
from utl_config import config


class DlgRfqBond:
    #private
    dlg = None

    def __init__(self, rfqid=''):
        self.dlg_rfq = uw.get_child_chk(app.wtop, name=r"RFQ Outright \[CANDEAL\/BOND\] \[\d+\]", ctrl_type='Pane', deep=1, use_re=1)  
   
    def press(self, but_name):
        butt = uw.get_child_chk(self.dlg_rfq, name=but_name, ctrl_type='Button', deep=1)  
        uw.win_click(butt)


