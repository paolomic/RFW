*** Settings ***
Documentation       Session Suite: CanDeal Bond Rfq: BuySide SellSide
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_rfq.py


*** Variables ***
${cfg_file}         ../utils/test/test_cd_rfq.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # sample array
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome     # sample dictionary
${rfqid}            000000000000                                        # sample var, result


*** Test Cases ***
# Note:
#   [Timeout] non funziona. Se func dura di piu si allupa RIDE

Prepare Test
    [Documentation]     Reset Environment
    [Timeout]           1 minutes
    ${timeout}=         Set Variable  30
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_prepare_test','${arg}','${cfg_file}','', ${timeout})  
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok


Coh: Prepare Session
    [Documentation]     launch process
    ${timeout}=         Set Variable  120
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_coh_prepare_session','${arg}','${cfg_file}','coh:new', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Web: Start New Session
    [Documentation]     Web login
    ${timeout}=         Set Variable  120
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_login_session','${arg}','${cfg_file}','web:new', ${timeout})  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_open_rfq','${arg}','${cfg_file}','web:hang')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Web: Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_send_rfq','${arg}','${cfg_file}','web:hang')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Coh: SellSide Reply
    [Documentation]     Accept RFQ
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_coh_reply','${arg}','${cfg_file}', 'coh:hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    [Timeout]           5 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_web_manage_rfq','${arg}','${cfg_file}','web:hang')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

