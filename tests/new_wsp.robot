*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_new.py  AS  test_new


*** Variables ***
&{opts}             speed=1    run=local    reuse_wsp=yes  save_wsp_onclose=yes                                                       # list of Suite Options
@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=C:/work/disks/D/COH_x64/bin/Coherence.exe    title=Starting Coherence
${orderid}          000000000000


*** Test Cases ***
Start New Session
    [Documentation]     launch process
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_session','${arg}',${opts},'new')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Starting Dialog
    [Documentation]     select addin list, version
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}         # Set Argument
    &{result}=          evaluate      test_new.robot_run('do_start_dialog',${arg},${opts}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Setting Init
    [Documentation]     set wsp, trace, level
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_setting_init','${arg}',${opts}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Start Connection
    [Documentation]     Enable Connections On, wait for Connection Ready
    [Timeout]           4 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_start_connections','${arg}',${opts}) 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Search Security
    [Documentation]     Search Security, open New Care Dialog
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_search_security','${arg}',${opts}) 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

New Care Order
    [Documentation]     fill care order and send, Retrieve new OrderID 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_care_order','${arg}',${opts}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    Set Suite Variable  ${orderid}    ${info}               # Use return Value
    Should Not Be Empty               ${orderid}
    
Select Order Row
    [Documentation]     Select New OrderID row in Page Apply Filter
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}            # Set Argument
    &{result}=          evaluate      test_new.robot_run('do_select_order','${arg}',${opts}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Grid Operation Sample
    [Documentation]     Test grid operation: header get, import rows, sort, search row
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_grid_sample','${arg}',${opts}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Session Close
    [Documentation]     Close Session and Check
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_close_session','${arg}',${opts},'kill') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok



