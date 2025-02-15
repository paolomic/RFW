*** Settings ***
Documentation       Session Suite: CanDeal Bond Rfq: BuySide SellSide
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_rfq.py


*** Variables ***
${cfg_file}         ../utils/test/test_cd_rfq.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # unused
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome     #unused
${rfqid}            000000000000                                        #unused


*** Test Cases ***
########### Coh: test
Coh: Start New Session
    [Documentation]     launch process
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_ss_new_session','${arg}','${cfg_file}','coh:new')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Coh: Starting Dialog
    [Documentation]     select addin list, version
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_ss_start_dialog','${arg}','${cfg_file}', 'coh:hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Coh: Setting Init
    [Documentation]     set wsp, trace, level
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_ss_setting_init','${arg}','${cfg_file}', 'coh:hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Coh: Start Connection
    [Documentation]     Enable Connections On, wait for Connection Ready
    [Timeout]           4 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_ss_start_connections','${arg}','${cfg_file}', 'coh:hang') 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

########### Web: test

Web: Start New Session
    [Documentation]     login
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_login_session','${arg}','${cfg_file}','web:')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_open_rfq','${arg}','${cfg_file}','web:')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

Web: Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_send_rfq','${arg}','${cfg_file}','web:')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok


Coh: Reply Coherence - SellSide
    [Documentation]     
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_ss_reply','${arg}','${cfg_file}', 'coh:hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Web: Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    [Timeout]           5 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_rfq.robot_run('do_manage_rfq','${arg}','${cfg_file}','web:')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

