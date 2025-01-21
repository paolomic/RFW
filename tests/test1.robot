*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_coh.py  AS  test_coh


*** Variables ***
@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=C:/work/disks/D/COH_x64/bin/Coherence.exe    title=Starting Coherence
${orderid}          000000000000


*** Test Cases ***
Launch New Session
    [Documentation]     Start New Coherence Session
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_launch_new_session('${arg}')  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Starting Dialog
    [Documentation]     Starting Dialog
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}xx
    &{result}=          evaluate      test_coh.robot_start_dialog("${arg}")  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Setting Dialog
    [Documentation]     Workspace Setting Initialization
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_setting_init('${arg}')  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Start Connections
    [Documentation]     Start Connections - Starting Addins and Console Connections
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_start_connections('${arg}')  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Security Browser
    [Documentation]     Security Browser - Search Security - command New Care Order
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_security_browser('${arg}')  modules=test_coh
    log                               result: &{result}
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

New Care Order
    [Documentation]     New Care Order 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_new_care_order('${arg}')  modules=test_coh
    log                               result: ${result}
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Set Suite Variable  ${orderid}    ${info}
    Should Be Equal As Strings  ${status}  ok

Select Order Row
    [Documentation]     Select Order Row - Use Prev Test OrderID
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}
    &{result}=          evaluate      test_coh.robot_select_order('${arg}')  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Grid Operation Sample
    [Documentation]     Grid Operation Sample - remote MFC Calls 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.grid_operation_sample('${arg}')  modules=test_coh
    ${status}=          evaluate      $result.status
    ${info}=            evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok