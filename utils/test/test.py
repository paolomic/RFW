
import sys
#from pathlib import Path

from datetime import datetime

from win32gui import GetCursorInfo
import time
import re


p = 'Do you want to save the page.*before closing.*'
t = 'Do you want to save the page\n"Orders: [*][*][*]" before closing?'

print(re.match(p, t.replace('\n', ' ')))

exit()

a = 'No. of Rows: 3'



print(re.match('No\.\ *of ([a-zA-Z0-9_]*): *([0-9])', a)[2])


exit()


#perform task that will make cursor busy
input("Press Enter to continue...")
time.sleep(0.2)
cursor_info = GetCursorInfo() #Get the current status of the cursor
normal_handle = cursor_info[1] #Get the normal cursor handle
current_handle = None

while current_handle != normal_handle:
    cursor_info = GetCursorInfo() #Get the current status of the cursor
    print(cursor_info)
    #current_handle = cursor_info[1] #Get the normal cursor handle
    #if current_handle != normal_handle:
    #    print("Cursor is busy. Normal cursor handle: " + str(normal_handle) + ", Current cursor handle: " + str(current_handle) + ".")
    time.sleep(0.5)
print("Cursor is not busy.")
