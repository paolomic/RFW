
from pywinauto import mouse
import keyboard
import time
import pywinauto

# import da altri path - MAMMAMIA :(
import sys
from pathlib import Path
_path_import = str(Path(__file__).parent.parent)
sys.path.append(_path_import) 

import utl_win as uw
import utl_old as uo


def send_key_sequence(seq:str):
  for c in seq:
    print(c)
    keyboard.press(c)
    time.sleep(0.5)
    keyboard.release(c)
    time.sleep(0.5)
  

#send_key_sequence('Prova')



wnd = uw.find_window(name="Google Chrome - Paolo", exact_match=False)
print (wnd)

uw.win_activate(wnd)


#cld = uw.get_child(wnd, name='.*pieghevole.*', recursive=True,use_regex=True)
#print (cld)

cld = uw.get_child(wnd, ctrl_type='Pane', recursive=False)
print (cld)


#####################
# Positions
#####################
cld_SEE = uw.get_child(wnd, name='Salesforce - Enterprise Edition', recursive=True, use_regex=False)    #Sub Window
print (f'cld_SEE {cld_SEE}')

cld_TEC = uw.get_child(cld_SEE, name='Time Entry .* Cancel', recursive=True, use_regex=True)            # sub window
print (f'cld_TEC {cld_TEC}')


#####################
# Activity
#####################

# hlink piu annidato
# Edit e LIST stanno sotto SEE


head = uw.get_child(cld_SEE, name='Activity', ctrl_type='Header', recursive=True, use_regex=False)
print (f'head {head}')

node = head.parent()
print (f'node {node}')

hlink = uw.get_child(node.parent(), ctrl_type='Hyperlink', recursive=True, use_regex=False)
print (f'hlink {hlink}')
coord = uw.win_click(hlink, wait=0.2)
time.sleep(1)

edit = uw.get_child(cld_SEE, ctrl_type='Edit', recursive=True, use_regex=False)
print (f'edit {edit}')

uw.win_click(edit)
value = "ftx"
keyboard.write(value, delay=0.05)
time.sleep(1)

list = uw.get_child(cld_SEE, ctrl_type='List', recursive=True, use_regex=False)   # la lista viene generata fuori sottoalbero, sotto Document - TODO ricerca anche per TEXTS
print (f'list {list}')
uw.dump_uia_path(list)
#print(uw.dump_uia_item(list))
uw.list_select(list, "ION Internal Development", "FTX", 'Markets - Developer')

time.sleep(4) # long wait - change layout

#####################
# ION Product
#####################
head = uw.get_child(cld_TEC, name='ION Product', ctrl_type='Header', recursive=True, use_regex=False)
print (f'head {head}')

combo = uw.get_child(head.parent(), ctrl_type='ComboBox', recursive=True, use_regex=False)
print(uw.dump_uia_item(combo))

data = uw.get_child(head.parent(), ctrl_type='DataItem', recursive=True, use_regex=False)
print (f'data {data}')

uw.win_click(combo)
time.sleep(0.5)

value = "IONM.FI.FTX"
keyboard.write(value, delay=0.05)
keyboard.send('enter')

# controllo valore
data = uw.win_reload_bytype(data)
assert value==data.window_text()
  
# non serve accedere alla lista - creata dinamicamente - ma non e' tutta visibile 
#list = uw.get_child(combo, ctrl_type='List', recursive=False, use_regex=False)
#print (f'list {list}')





exit()



