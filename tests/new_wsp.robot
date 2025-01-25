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
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_session','${arg}',True)  
    log                               result: ${result}
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok
    
Starting Dialog
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}
    &{result}=          evaluate      test_new.robot_run('do_start_dialog','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok

Setting Init
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_setting_init','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok

Start Connection
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_start_connections','${arg}') 
    log                               result: ${result}
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok

Search Security
    [Documentation]     nope
    [Timeout]           2 minutes
    &{result}=          evaluate      test_new.robot_run('do_search_security','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok

New Care Order
    [Documentation]     nope 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_care_order','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}
    
Select Order Row
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}
    &{result}=          evaluate      test_new.robot_run('do_select_order','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok
    
Grid Operation Sample
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_grid_sample','${arg}') 
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        ${status}     ok




