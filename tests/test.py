import keyboard
import mouse
import time


import traceback
#TODO Spostare questo py in tests/modules (problema include)    





# Import 
import sys
from pathlib import Path
#_new_path = str(Path(__file__).parent.parent)
#sys.path.append(_new_path) 
strpath = r'C:\work\disks\D\prog\RFW\utils'
sys.path.append(strpath) 

import utl  as utl
from utl_app import env, opt, VERIFY, RAISE, DUMP
from utl_win import sleep, ROBOT_RES
import utl_win as uw
import utl_log as ul
import utl_grid as ug
import utl_dump as ud


if __name__ == '__main__':
    def fun1():
        print(3/0)

    def fun2():
        q = 4+ 3
        fun1()

    def fun3():
        # something
        fun2()

    try:
        fun3()
    except Exception as e:
        print("Traceback:")
        traceback.print_exc()
        DUMP( str(e))