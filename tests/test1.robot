*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             test.py
Library  ../utils/test/test_coh.py  AS  test_coh

**Variables**
${orderid}          000000000000

*** Test Cases ***
Launch New Session
    [Documentation]     Start Coherence Session
    [Timeout]           2 minutes
    ${arg}=             Set Variable    no need any var
    &{result}=          evaluate        test_coh.robot_launch_new_session('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Starting Dialog
    [Documentation]     Starting Dialog
    [Timeout]           2 minutes
    ${arg}=             Set Variable    no need any var
    &{result}=          evaluate        test_coh.robot_start_dialog('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Setting Dialog
    [Documentation]     Workspace Setting Initialization
    [Timeout]           2 minutes
    ${arg}=             Set Variable    no need any var
    &{result}=          evaluate        test_coh.robot_setting_init('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Start Connections
    [Documentation]     Starting Addins and Console Connections
    [Timeout]           2 minutes
    ${arg}=             Set Variable    MetaMarket
    &{result}=          evaluate        test_coh.robot_start_connections('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Security Browser
    [Documentation]     Search Security 
    [Timeout]           2 minutes
    ${arg}=             Set Variable    noarg
    &{result}=          evaluate        test_coh.robot_security_browser('${arg}')  modules=test_coh
    log                 result: &{result}
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

New Care Order
    [Documentation]     New Care Order 
    [Timeout]           2 minutes
    ${arg}=             Set Variable    noarg
    &{result}=          evaluate        test_coh.robot_new_care_order('${arg}')  modules=test_coh
    log  result: ${result}
    ${status}=  evaluate    $result.status
    ${info}=  evaluate      $result.info
    Set Suite Variable  ${orderid}  ${info}
    Should Be Equal As Strings  ${status}  ok

Select Order Row - Use OrderId
    [Documentation]     Select Order Row 
    [Timeout]           2 minutes
    ${arg}=             Set Variable    ${orderid}
    &{result}=          evaluate        test_coh.robot_select_order('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok

Grid Operation Sample
    [Documentation]     Grid Operation Sample remote MFC Calls 
    [Timeout]           2 minutes
    ${arg}=             Set Variable    Nope
    &{result}=          evaluate        test_coh.grid_operation_sample('${arg}')  modules=test_coh
    ${status}=  evaluate      $result.status
    ${info}=  evaluate      $result.info
    Should Be Equal As Strings  ${status}  ok