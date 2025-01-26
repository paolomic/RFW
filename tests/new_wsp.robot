*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_new.py  AS  test_new


*** Variables ***
@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=C:/work/disks/D/COH_x64/bin/Coherence.exe    title=Starting Coherence
${orderid}          000000000000


*** Test Cases ***
Start New Session
    [Documentation]     launch process
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_session','${arg}','new')  
    log                               result: ${result}
    ${info}=            evaluate      ${result.info}
    log                               info: ${info}
    Should Be Equal As Strings        ${result.status}     ok
    
Starting Dialog
    [Documentation]     select addin version
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}
    &{result}=          evaluate      test_new.robot_run('do_start_dialog','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Setting Init
    [Documentation]     set wsp trace level
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_setting_init','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Start Connection
    [Documentation]     press connection On, wait for Connection Ready
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_start_connections','${arg}') 
    log                               result: ${result}
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Search Security
    [Documentation]     Search Security, open New Care Dialog
    [Timeout]           2 minutes
    &{result}=          evaluate      test_new.robot_run('do_search_security','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

New Care Order
    [Documentation]     fill care order and send, retrieve new OrderID 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_care_order','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}
    
Select Order Row
    [Documentation]     Select New OrderID row in Page
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}
    &{result}=          evaluate      test_new.robot_run('do_select_order','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok
    
Grid Operation Sample
    [Documentation]     test grid operation, header import sort search
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_grid_sample','${arg}') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Session Close
    [Documentation]     Close Session
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_close_session','${arg}','kill') 
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok



