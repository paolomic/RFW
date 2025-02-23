

#region - import

import keyboard
import mouse

# Import utils
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent)
sys.path.append(_new_path) 

# util modules
import utl as utl
from utl_config import config
from utl_app import app
from utl_web import wapp
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_run as ur
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud

# page modules
from page_console           import PageSettings
from page_addin_sellside    import DlgRfqBond
from page_web               import WebDlgRfqBond

if __name__ == '__main__':
    wapp.launch_url(config.get('web.url'))
    edit = uw.get_child_retry(wapp.doc, name='USERNAME.*', automation_id='username', ctrl_type='Edit', use_re=1, retry_timeout=8)
    print (edit)