
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
import utl_dump as ud

def kimble(SerchKey, ActivKey:list, IONProduct, Activity, Notes, Hours):
    ###############################
    # region - Windows

    wnd = uw.find_window(name="Google Chrome - Paolo", exact_match=False)
    print (f'wnd {wnd}')
    uw.win_activate(wnd)

    #endregion

    ###############################
    # region - PlaceHolders

    node_SEE = uw.get_child(wnd, name='Salesforce - Enterprise Edition', deep=8)    #Sub Window
    print (f'node_SEE {node_SEE}')

    node_TEC = uw.get_child(node_SEE, name='Time Entry .* Cancel', deep=8, use_re=True)           # sub window - dopo c e anche Save
    print (f'node_TEC {node_TEC}')

    #ud.dump_uia_tree(node_TEC)

    #endregion

    ###############################
    # region - Activity

    if (SerchKey):
        # hyperlink piu annidato
        # Edit e LIST (dinamiche?) sotto SEE

        head = uw.get_child(node_SEE, name='Activity', ctrl_type='Header', deep=8)
        print (f'head {head}')

        node = head.parent()
        print (f'node {node}')

        hlink = uw.get_child(node.parent(), ctrl_type='Hyperlink', deep=8)
        print (f'hlink {hlink}')
        coord = uw.win_click(hlink)
        time.sleep(1)

        edit = uw.get_child(node_SEE, ctrl_type='Edit', deep=8)
        print (f'edit {edit}')
        uw.win_click(edit)

        value = SerchKey
        keyboard.write(value, delay=0.05)

        list = uw.get_child_retry(node_SEE, ctrl_type='List', deep=8, wait_init=1, wait_end=0.5) 
        print (f'list {list}')
        #ud.dump_uia_path(list)
        uw.list_select_texts(list, ActivKey)

        # UIA changes dinamically here 

    #endregion

    ###############################
    # region - ION Product 

    if (IONProduct):
        head = uw.get_child_retry(node_TEC, name='ION Product', ctrl_type='Header', deep=8, wait_init=4, wait_end=0.5)
        print (f'head {head}')

        combo = uw.get_child(head.parent(), ctrl_type='ComboBox', deep=8)
        #print(ud.dump_uia_item(combo))

        data = uw.get_child(head.parent(), ctrl_type='DataItem', deep=8)   # solo per check
        print (f'data {data}')

        uw.win_click(combo, wait_end=0.5)

        value = IONProduct
        keyboard.write(value, delay=0.05)
        keyboard.send('enter')

        # controllo valore
        data = uw.win_reload_bytype(data)
        assert value==data.window_text()
            
        # non serve accedere alla lista - creata dinamicamente - ma non e' tutta visibile 
        #list = uw.get_child(combo, ctrl_type='List', recursive=False)
        #print (f'list {list}')
    #endregion

    ###############################
    # region - Activity/Roadmap Type

    if (Activity):
        head = uw.get_child(node_TEC, name='Activity/Roadmap Type', ctrl_type='Header', deep=8)
        print (f'head {head}')

        node = head.parent()    # Custom

        combo = uw.get_child(node, ctrl_type='ComboBox', deep=8)
        print (f'combo {combo}')

        uw.win_click(combo, wait_end=0.5)

        list = uw.get_child(node, ctrl_type='List', deep=8)
        print (f'list {list}')
        #ud.dump_uia_tree(list)
        assert uw.list_select(list, Activity, use_re=True)

        # Metodo Alternativo - Digito una substr della selezione - Quando la lista e' scollabile - non tutta a video
        #value = Activity
        #keyboard.write(value, delay=0.05)
        #keyboard.send('enter')

        # todo - check selection

    #endregion

    ###############################
    # region - Notes

    if (Notes):
        head = uw.get_child(node_TEC, name='Notes', ctrl_type='Header', deep=8)
        print (f'head {head}')

        edit = uw.get_child(head.parent(), ctrl_type='Edit', deep=8)
        print (f'edit {edit}')

        uw.win_click(edit)

        value = Notes
        keyboard.write(value, delay=0.05)
    
    #endregion

    ###############################
    # region - Hours

    if (Hours):
        head = uw.get_child(node_TEC, name='Entry Hours', ctrl_type='Header', deep=8)
        print (f'head {head}')

        edit = uw.get_child(head.parent(), ctrl_type='Edit', deep=8)
        print (f'edit {edit}')

        uw.win_click(edit)

        value = Hours
        keyboard.write(value, delay=0.05)

    #endregion

    ###############################
    # region - TrackerRefID - CONSTANT

    head = uw.get_child(node_TEC, name='Tracker Ref ID', ctrl_type='Header', deep=8)
    print (f'head {head}')

    edit = uw.get_child(head.parent(), ctrl_type='Edit', deep=8)
    print (f'edit {edit}')

    uw.win_click(edit)

    value = "none"
    keyboard.write(value, delay=0.05)

    #endregion

    ###############################
    # region - Save Butt

    butt = uw.get_child(node_TEC, name='Save', ctrl_type='Button', automation_id='saveNewEntryBtn', deep=8)
    print (f'butt {butt}')
    #uw.dump_uia_path(butt)
    mouse.move(uw.win_coord(butt))

    #endregion

#kimble('ftx', ['ION Internal Development', 'FTX', 'Markets - Developer'], 'IONM.FI.FTX', 'Support', 'MyNotes', '0.5')
kimble('ftx', ['ION Internal Development', 'FTX', 'Markets - Developer'], 'IONM.FI.FTX', '.evelopment.*Incremental', 'MyNotes', '0.5')
