
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

def kimble(key, s1, s2, s3, IONProduct, Activity, Notes, Hours):
    #####################
    # Windows
    #####################
    wnd = uw.find_window(name="Google Chrome - Paolo", exact_match=False)
    print (f'wnd {wnd}')
    uw.win_activate(wnd)

    #####################
    # Positions
    #####################
    node_SEE = uw.get_child(wnd, name='Salesforce - Enterprise Edition', recursive=True, use_regex=False)    #Sub Window
    print (f'node_SEE {node_SEE}')

    node_TEC = uw.get_child(node_SEE, name='Time Entry .* Cancel', recursive=True, use_regex=True)            # sub window - dopo c e anche Save
    print (f'node_TEC {node_TEC}')

    #uw.dump_uia_tree(node_TEC)

    ###############################
    # Activity
    ###############################
    if (key):
      # hyperlink piu annidato
      # Edit e LIST (dinamiche?) sotto SEE

      head = uw.get_child(node_SEE, name='Activity', ctrl_type='Header', recursive=True, use_regex=False)
      print (f'head {head}')

      node = head.parent()
      print (f'node {node}')

      hlink = uw.get_child(node.parent(), ctrl_type='Hyperlink', recursive=True, use_regex=False)
      print (f'hlink {hlink}')
      coord = uw.win_click(hlink, wait=0.2)
      time.sleep(1)

      edit = uw.get_child(node_SEE, ctrl_type='Edit', recursive=True, use_regex=False)
      print (f'edit {edit}')
      uw.win_click(edit)

      value = key
      keyboard.write(value, delay=0.05)
      time.sleep(1)

      list = uw.get_child(node_SEE, ctrl_type='List', recursive=True, use_regex=False)   # la lista viene generata fuori sottoalbero, sotto Document - TODO ricerca anche per TEXTS
      print (f'list {list}')
      uw.dump_uia_path(list)
      #print(uw.dump_uia_tree(list))
      uw.list_select_texts(list, s1, s2, s3)

      time.sleep(4.5) # long wait - change layout - TODO inteligent wait

    ###############################
    # ION Product
    ###############################
    if (IONProduct):
      head = uw.get_child(node_TEC, name='ION Product', ctrl_type='Header', recursive=True, use_regex=False)
      print (f'head {head}')

      combo = uw.get_child(head.parent(), ctrl_type='ComboBox', recursive=True, use_regex=False)
      print(uw.dump_uia_item(combo))

      data = uw.get_child(head.parent(), ctrl_type='DataItem', recursive=True, use_regex=False)   # solo per check
      print (f'data {data}')

      uw.win_click(combo)
      time.sleep(0.5)

      value = IONProduct
      keyboard.write(value, delay=0.05)
      keyboard.send('enter')

      # controllo valore
      data = uw.win_reload_bytype(data)
      assert value==data.window_text()
        
      # non serve accedere alla lista - creata dinamicamente - ma non e' tutta visibile 
      #list = uw.get_child(combo, ctrl_type='List', recursive=False, use_regex=False)
      #print (f'list {list}')

    ###############################
    # Activity/Roadmap Type
    ###############################
    if (Activity):
      head = uw.get_child(node_TEC, name='Activity/Roadmap Type', ctrl_type='Header', recursive=True, use_regex=False)
      print (f'head {head}')

      node = head.parent()    # Custom

      combo = uw.get_child(node, ctrl_type='ComboBox', recursive=True, use_regex=False)
      print (f'combo {combo}')

      uw.win_click(combo)
      time.sleep(0.5)

      list = uw.get_child(node, ctrl_type='List', recursive=True, use_regex=False)
      print (f'list {list}')
      uw.dump_uia_tree(list)

      value = Activity
      keyboard.write(value, delay=0.05)
      keyboard.send('enter')

      #uw.list_select(list, "Support")

      ###############################
      # Notes
      ###############################
      if (Notes):
        head = uw.get_child(node_TEC, name='Notes', ctrl_type='Header', recursive=True, use_regex=False)
        print (f'head {head}')

        edit = uw.get_child(head.parent(), ctrl_type='Edit', recursive=True, use_regex=False)
        print (f'edit {edit}')

        uw.win_click(edit)
        time.sleep(0.5)

        value = Notes
        keyboard.write(value, delay=0.05)

     
      ###############################
      # Hours
      ###############################
      if (Hours):
        head = uw.get_child(node_TEC, name='Entry Hours', ctrl_type='Header', recursive=True, use_regex=False)
        print (f'head {head}')

        edit = uw.get_child(head.parent(), ctrl_type='Edit', recursive=True, use_regex=False)
        print (f'edit {edit}')

        uw.win_click(edit)
        time.sleep(0.5)

        value = Hours
        keyboard.write(value, delay=0.05)

      ###############################
      # TrackerRefID - CONSTANT
      ###############################
      head = uw.get_child(node_TEC, name='Tracker Ref ID', ctrl_type='Header', recursive=True, use_regex=False)
      print (f'head {head}')

      edit = uw.get_child(head.parent(), ctrl_type='Edit', recursive=True, use_regex=False)
      print (f'edit {edit}')

      uw.win_click(edit)
      time.sleep(0.5)

      value = "none"
      keyboard.write(value, delay=0.05)

      ###############################
      # Save Butt
      ###############################
      butt = uw.get_child(node_TEC, name='Save', ctrl_type='Button', automation_id='saveNewEntryBtn', recursive=True, use_regex=False)
      print (f'butt {butt}')
      #uw.dump_uia_path(butt)
      mouse.move(uw.win_coord(butt))


#kimble('ftx', 'ION Internal Development', 'FTX', 'Markets - Developer', 'IONM.FI.FTX', 'Support', 'MyNotes', '0.5')
kimble('ftx', 'ION Internal Development', 'FTX', 'Markets - Developer', 'IONM.FI.FTX', 'Support', 'MyNotes', '0.5')
