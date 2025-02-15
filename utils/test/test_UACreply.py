import keyboard
import mouse
import time

#TODO Spostare questo py in tests/modules (problema include)



#strpath = r'C:\work\disks\D\prog\RFW\utils'
#sys.path.append(strpath) 

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl
from utl_app import app, opt
from utl_verifier import VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud

COH_SETUP = r'C:\Users\Paolo.Michetti\OneDrive - ION\Desktop\CanDeal evolutionSetup_x64_25_6.0.0d3.exe'


def main():
    cmd = uw.get_main_wnd('.*System32.*py.*test_UAC.py')
    print(cmd)
    cmd.set_focus()
    keyboard.write('Peperone,121212')
    keyboard.press_and_release('enter')
    

if __name__ == "__main__":
    main()