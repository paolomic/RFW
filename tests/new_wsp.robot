*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_new_wsp.py  AS  test_new


*** Variables ***
${cfg_file}         ../utils/test/test_new_wsp.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # sample array
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome     # sample dictionary
${orderid}          000000000000


*** Test Cases ***
Common: Prepare Test
    [Documentation]     Reset Environment Applications
    &{req}              Create Dictionary   fun=do_prepare_test  arg=   coh=terminate   web=terminate   timeout=60
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Start New Session
    [Documentation]     launch process
    &{req}              Create Dictionary   fun=do_coh_new_session  arg=   coh=new   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
    
Starting Dialog
    [Documentation]     select addin list, version
    &{req}              Create Dictionary   fun=do_coh_start_dialog  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Setting Init
    [Documentation]     set wsp, trace, level
    &{req}              Create Dictionary   fun=do_coh_setting_init  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Start Connection
    [Documentation]     Enable Connections On, wait for Connection Ready
    &{req}              Create Dictionary   fun=do_coh_start_connections  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Search Security
    [Documentation]     Search Security, open New Care Dialog
    &{req}              Create Dictionary   fun=do_coh_search_security  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

New Care Order
    [Documentation]     fill care order and send, Retrieve new OrderID 
    &{req}              Create Dictionary   fun=do_coh_new_care_order  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
    Set Suite Variable  ${orderid}          ${info}                     # Use return Value
    Should Not Be Empty                     ${orderid}
    
Select Order Row
    [Documentation]     Select New OrderID row in Page Apply Filter     # Set Argument
    &{req}              Create Dictionary   fun=do_coh_select_order  arg=${orderid}   coh=hang   web=-   timeout=120     # Set Argument
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
    
Grid Operation Sample
    [Documentation]     Test grid operation: header get, import rows, sort, search row
    &{req}              Create Dictionary   fun=do_coh_grid_sample  arg=   coh=hang   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Session Close
    [Documentation]     Close Session and Check
    &{req}              Create Dictionary   fun=do_close_test  arg=   coh=close   web=-   timeout=120
    &{result}=          evaluate            test_new_wsp.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok


