*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_new.py  AS  test_new


*** Variables ***
${cfg_file}         ../utils/test/test_new_wsp.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # sample array
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome     # sample dictionary
${orderid}          000000000000


*** Test Cases ***
Common: Prepare Test
    [Documentation]     Reset Environment Applications
    [Timeout]           1 minutes     #dont work
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  60
    &{result}=          evaluate      test_cd_rfq.robot_run('do_prepare_test','${arg}','${cfg_file}','', ${timeout})  
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Start New Session
    [Documentation]     launch process
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_new_session','${arg}','${cfg_file}','coh:new', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Starting Dialog
    [Documentation]     select addin list, version
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_start_dialog',${arg},'${cfg_file}','coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Setting Init
    [Documentation]     set wsp, trace, level
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_setting_init','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Start Connection
    [Documentation]     Enable Connections On, wait for Connection Ready
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_start_connections','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Search Security
    [Documentation]     Search Security, open New Care Dialog
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_search_security','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

New Care Order
    [Documentation]     fill care order and send, Retrieve new OrderID 
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_new_care_order','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    Set Suite Variable  ${orderid}    ${info}               # Use return Value
    Should Not Be Empty               ${orderid}
    
Select Order Row
    [Documentation]     Select New OrderID row in Page Apply Filter
    ${arg}=             Set Variable  ${EMPTY}
    ${arg}=             Set Variable  ${orderid}            # Set Argument
    &{result}=          evaluate      test_new.robot_run('do_coh_select_order','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Grid Operation Sample
    [Documentation]     Test grid operation: header get, import rows, sort, search row
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_coh_grid_sample','${arg}','${cfg_file}','coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Session Close
    [Documentation]     Close Session and Check
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_new.robot_run('do_close_test','${arg}','${cfg_file}','coh:hang,kill', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok



