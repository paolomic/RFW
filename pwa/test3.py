from util import *

from util_ocr2 import *


#WIN_TITLE = "Starting Coherence.*" 
APP_TITLE = "Coherence.*DEBUG.*" 
WIN_TITLE = "Trades.*" 

# Esempio - Aggancio App gi a partita

wnd_coh = get_main_wnd(APP_TITLE, timeout_sec=1)
    
if not wnd_coh:
  raise TypeError("ERROR: no Coherence Application")

main_title = wnd_coh.window_text()
app_coh = Application(backend="uia").connect(title=main_title)
print (f'Connected {main_title}')

wnd_trade1 = get_single_child_wnd(wnd_coh, WIN_TITLE, timeout_sec=1)    #Trade1
if not wnd_trade1:
  raise TypeError("ERROR: no Trade1 Windows")

print (type(wnd_trade1))

wnd_trade2 = get_single_child_wnd(wnd_trade1, "Trade.*", timeout_sec=1) #Trades: ....
if not wnd_trade2:
  raise TypeError("ERROR: no wnd_trade2 Windows")

wnd_trade3 =  wnd_trade2.children()[0]                   # Pane "" ""
if not wnd_trade3:
  raise TypeError("ERROR: no wnd_trade3 Windows")

wnd_trade4 =  wnd_trade3.children()[0]                   # Pane "" "59648"
if not wnd_trade4:
  raise TypeError("ERROR: no wnd_trade4Windows")

extract_grid_data_from_control(wnd_trade4)

print (type(wnd_trade4))
print (wnd_trade4.automation_id())

print("Ok")
#PrintAppTree(window)


#window.print_ctrl_ids()

#lista = window.child_window(title="Import From", auto_id="12458", control_type="List")
#if not lista:
#  raise TypeError("ERROR: no lista")

#list_check(lista, "MetaMarket")

#topp = get_main_window(lista)

#addins = listbox_to_json(lista)
#print (addins)

#list_check_mass(lista, "")
#toggle_list_item(lista, "MetaMarket")

#print(get_list_item_toggle_state(lista, "MetaMarket"))     # in testing non funziona



  


        