import keyboard
import mouse
import time

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
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
from page_metamarket        import PageSecurityBrowser, DlgNewCareOrder, PageOrders



######################################################
### Robot Operations
#region 

def do_prepare_test(arg):
    app.manage_conn('terminate', 'coh:all')
    sleep(1)

def do_coh_new_session(arg):
    if not config.get('opt.reuse_wsp')=='yes':
        app.reset_wsp()

def do_coh_start_dialog(arg):
    app.start_dialog(config.get('coh.wsp'), config.get('coh.addins'))                                          
    app.reload()                                                                            # Smart Wait for new Main Frame   
    uw.win_move(app.wtop, 8, 8)
    #app.connection(start=False)             # se riuso il wsp stacco la conn                                                                          # Smart Wait for new Main Frame   
        
def do_coh_setting_init(arg):
    setting_dlg = PageSettings()
    setting_dlg.open()
    ### Connection  - Disable se connection Ready
    setting_dlg.set_platform(config.get('coh.primary'), config.get('coh.port'), 
                             config.get('coh.user'),  config.get('coh.pass'),
                             config.get('coh.band_save') )
    setting_dlg.metamarket('detail')
    setting_dlg.workspace('detail')
    setting_dlg.close()

def do_coh_start_connections(arg):
    app.connection(start=True, addins = ['MetaMarket'])

def do_coh_search_security(arg):
    secbr = PageSecurityBrowser(new=1)
    secbr.tree_filter(config.get('coh.exc'), config.get('coh.mrk'))
    secbr.filter(config.get('coh.sec'))

    status_num = uw.page_get_num(secbr.wnd)                     # class astratta
    VERIFY(status_num==1, 'Not Such Unique Security') 

    # hide
    uw.win_click(secbr.grid, mode='grid_row1')
    mouse.click('right')
    sleep(0.2)

    uw.popup_reply(app.wtop, 'New#Care Order')                      # Il popup viene generato sotto level top - anche il sotto menu
    uw.page_save(secbr.wnd, 'security_search', time_tag=True)
    uw.page_close(secbr.wnd)

def do_coh_new_care_order(arg):
    newcare = DlgNewCareOrder()

    newcare.set_qty(config.get('coh.qty'))
    newcare.set_price(config.get('coh.price'))
    newcare.set_alias(config.get('coh.alias'))
    
    newcare.advanced(True)
    send_time = utl.get_now_sec()
    mytag = f'robot_{send_time.replace(":","_")}' 
    newcare.set_note(mytag)
    newcare.advanced(False)

    newcare.send()

    order = newcare.retrieve_orderid(mytag, send_time)
    VERIFY(order, 'Order not Found')

    newcare.close()
    
    return order['fields']['OrderID']
 
def do_coh_select_order(arg):
    order_id = arg
    print(f'order_id: {order_id}')
    
    orders = PageOrders(new=1)
    orders.clear_filter()
    orders.set_filter('Order ID', order_id)
    orders.apply_filter()

    status_num = uw.page_get_num(orders.wnd)                    # todo collocare ...
    VERIFY(status_num==1, 'Order Selection Failed') 

    uw.page_save(orders.wnd, 'order_filtered', time_tag=True)   # collocare

def do_coh_grid_sample(arg):                         
    secbr = PageSecurityBrowser(new=1)
    secbr.tree_filter(config.get('coh.exc'), config.get('coh.mrk'))
   
    # Esempio Get sheet info
    ug.set_show_all_2(app.wtop, secbr.grid)                         #collocalre ....
    grid_mng = ug.create_by_win(secbr.grid)
    
    # esempio scroll
    ug.scroll_home(grid_mng)

    # esempio column sort
    ug.set_sort(grid_mng,'default')
    ug.set_sort(grid_mng, [['Section','DESC'],['Security Ref.','ASC']])

    #esempio Import Rows
    ug.import_rows(grid_mng, 85, mode='row')
    #print(grid_mng.data['rows'])
    
    # esempio Data Row Search
    print (f'Collected Rows: {grid_mng.get_row_num()}')
    sel = grid_mng.search_first_match({"Description": config.get('coh.sec')})             # piu segmenti con , 
    print(f'Find {1 if sel else 0} Row')
    VERIFY(sel, 'Security not Found')
    
    print(f'Find Row: {sel}')
    print(f'Security Status: {sel["Status"]}')
    uw.page_save(secbr.wnd, 'security_grid_demo', time_tag=True)                           #collocalre ....

def do_close_test(arg):                         
    pass

#endregion


######################################################
# Generic Caller
def robot_run(req:dict, cfg_file:str):
    try:
        fun_name = req['fun']
        arg = req['arg']
        conn_coh = req['coh']
        conn_web = req['web']
        timeout = eval(req['timeout'])
        
        config.load(cfg_file)
        func = globals().get(fun_name)
    except Exception as e:
        exc_mess = str(e)
        DUMP(exc_mess)
        return ROBOT_RES('no', exc_mess)
    
    return ur.robot_run_3(func, arg, conn_coh, conn_web, timeout)       
######################################################
# Main DEBUG 

    
if __name__ == '__main__':
    cfg_file = r'.\utils\test\test_new_wsp.json'
    select = 3
    if (select==1):
        print(robot_run('do_web_login_session', '', cfg_file, '') )
    if (select==2):
        #do_web_login_session('')
        pass
    if (select==3):
        #ur.terminate_sessions()
        #print(robot_run('do_prepare_test', '', cfg_file, '', timeout=30) )
        #print(robot_run('do_coh_new_session', '', cfg_file, 'coh:new', timeout=66) )
        #print(robot_run('do_coh_start_dialog', '', cfg_file, 'coh:hang', timeout=66) )
        #print(robot_run('do_coh_setting_init', '', cfg_file, 'coh:hang', timeout=66) )
        #print(robot_run('do_coh_start_connections', '', cfg_file, 'coh:hang', timeout=120) )
        
        #print(robot_run('do_coh_search_security', '', cfg_file, 'coh:hang', timeout=120) )
        #print(robot_run('do_coh_new_care_order', '', cfg_file, 'coh:hang', timeout=120) )
        #print(robot_run('do_coh_select_order', 'C10022402280000010414', cfg_file, 'coh:hang', timeout=120) )
        print(robot_run('do_coh_grid_sample', '', cfg_file, 'coh:hang', timeout=120) )

