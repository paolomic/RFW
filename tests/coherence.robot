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
    &{result}=          evaluate      test_coh.robot_launch_new_session('${arg}')
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Starting Dialog
    [Documentation]     Starting Dialog
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}
    &{result}=          evaluate      test_coh.robot_start_dialog("${arg}")
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Setting Dialog
    [Documentation]     Workspace Setting Initialization
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_setting_init('${arg}')
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Start Connections
    [Documentation]     Start Connections - Starting Addins and Console Connections
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_start_connections('${arg}')
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

Security Browser
    [Documentation]     Security Browser - Search Security - command New Care Order
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_security_browser('${arg}')
    log                               result: &{result}
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok

New Care Order
    [Documentation]     New Care Order 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_new_care_order('${arg}')
    log                               result: ${result}
    ${info}=            evaluate      ${result.info}
    Should Be Equal As Strings        ${result.status}     ok
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}

Select Order Row
    [Documentation]     Select Order Row - Use Prev Test OrderID
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${orderid}
    &{result}=          evaluate      test_coh.robot_select_order('${arg}')
    ${status}=          evaluate      $result.status
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}

Grid Operation Sample
    [Documentation]     Grid Operation Sample - remote MFC Calls 
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_coh.robot_grid_sample('${arg}')
    ${status}=          evaluate      $result.status
    Set Suite Variable  ${orderid}    ${info}
    Should Not Be Empty               ${orderid}
