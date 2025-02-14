*** Settings ***
Documentation       CanDeal BuySide -  Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_bs.py


*** Variables ***
&{opts}             speed=110    run=local    reuse_wsp=yes  save_wsp_onclose=yes  close_all_pages=yes                                                    # list of Suite Options
#@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome
${ftqid}            000000000000


*** Test Cases ***
Start New Session
    [Documentation]     login
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_login_session','${arg}',${opts},'')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_open_rfq','${arg}',${opts},'')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_send_rfq','${arg}',${opts},'')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    [Timeout]           5 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_manage_rfq','${arg}',${opts},'')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok