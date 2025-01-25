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
Launch New Session
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_session','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok
    

Starting Dialog
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}
    &{result}=          evaluate      test_new.robot_run('do_start_dialog','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok

Setting Init
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_setting_init','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok


Start Connection
    [Documentation]     nope 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_start_connections','${arg}') 
    log                               result: ${result}
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok

Search Security
    [Documentation]     nope
    [Timeout]           2 minutes
    &{result}=          evaluate      test_new.robot_run('do_search_security','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok

New Care Order
    [Documentation]     nope 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_new_care_order','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}
    
Select Order Row
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}
    &{result}=          evaluate      test_new.robot_run('do_select_order','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok
    
Grid Operation Sample
    [Documentation]     nope
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_grid_sample','${arg}') 
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings        $result.status     ok




