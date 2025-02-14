*** Settings ***
Documentation       CanDeal BuySide -  Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_bs.py


*** Variables ***
&{opts}             speed=110    run=local    reuse_wsp=no  save_wsp_onclose=yes  close_all_pages=yes                                                    # list of Suite Options
@{addin_list}       MetaMarket  FQ SellSide  UserPages
#@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=http://10.91.204.20/login    driver=Chrome
${ftqid}            000000000000


*** Test Cases ***

########### Coh Start
COH Start New Session
    [Documentation]     launch process
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_ss_new_session','${arg}',${opts},'new')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
COH Starting Dialog
    [Documentation]     select addin list, version
    [Timeout]           2 minutes
    ${arg}=             Set Variable  @{addin_list}         # Set Argument
    &{result}=          evaluate      test_cd_bs.robot_run('do_ss_start_dialog',${arg},${opts}, 'hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

COH Setting Init
    [Documentation]     set wsp, trace, level
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_ss_setting_init','${arg}',${opts}, 'hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

COH Start Connection
    [Documentation]     Enable Connections On, wait for Connection Ready
    [Timeout]           4 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_ss_start_connections','${arg}',${opts}, 'hang') 
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

########### Web Start

WEB Start New Session
    [Documentation]     login
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_login_session','${arg}',${opts},'web')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
WEB Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_open_rfq','${arg}',${opts},'web')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

WEB Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_send_rfq','${arg}',${opts},'web')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok


COH Reply Coherence - SellSide
    [Documentation]     
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_ss_reply','${arg}',${opts}, 'hang') 
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    
WEB Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    [Timeout]           5 minutes     #slow
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_cd_bs.robot_run('do_manage_rfq','${arg}',${opts},'web')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

