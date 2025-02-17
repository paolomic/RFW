*** Settings ***
Documentation       Session Suite: CanDeal Bond Rfq: BuySide SellSide
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_rfq.py


*** Variables ***
${cfg_file}         ../utils/test/test_cd_rfq.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # sample array
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome     # sample dictionary

*** Test Cases ***
# Note:
#   [Timeout] non funziona. Se func dura di piu si allupa RIDE

Common: Prepare Test
    [Documentation]     Reset Environment Applications
    [Timeout]           1 minutes     #dont work
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  60
    &{result}=          evaluate      test_cd_rfq.robot_run('do_prepare_test','${arg}','${cfg_file}','', ${timeout})  
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Coh: Prepare Session
    [Documentation]     launch process
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_coh_prepare_session','${arg}','${cfg_file}','coh:new', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Web: Start New Session
    [Documentation]     Web login
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_login_session','${arg}','${cfg_file}','web:new', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_open_rfq','${arg}','${cfg_file}','web:hang', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Web: Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_send_rfq','${arg}','${cfg_file}','web:hang', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Coh: SellSide Reply
    [Documentation]     Accept RFQ
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_coh_reply','${arg}','${cfg_file}', 'coh:hang', ${timeout}) 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    ${arg}=             Set Variable  ${EMPTY}
    ${timeout}=         Set Variable  120
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_manage_rfq','${arg}','${cfg_file}','web:hang', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

