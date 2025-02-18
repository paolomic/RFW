*** Settings ***
Documentation       Session Suite: CanDeal Bond Rfq: BuySide SellSide
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_rfq.py


*** Variables ***
${cfg_file}         ../utils/test/test_cd_rfq.json
@{addin_list}       MetaMarket  FQ SellSide  UserPages                  # sample array
&{req_dict}         fun=do_prepare_test   coh=terminate   web=terminate   timeout=60     # sample dictionary

*** Test Cases ***
# Note:
#   [Timeout] non funziona. Se func dura di piu si allupa RIDE

Common: Prepare Test
    [Documentation]     Reset Environment Applications
    &{req}              Create Dictionary   fun=do_prepare_test  arg=   coh=terminate   web=terminate   timeout=60
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Coh: Prepare Session
    [Documentation]     launch process
    &{req}              Create Dictionary   fun=do_coh_prepare_session  arg=   coh=new   web=   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Web: Start New Session
    [Documentation]     Web login
    &{req}              Create Dictionary   fun=do_web_login_session  arg=   coh=   web=new   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
    
Web: Open Rfq Panel
    [Documentation]     Open New Rfq Panel
    &{req}              Create Dictionary   fun=do_web_open_rfq  arg=   coh=   web=hang   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Web: Send a New Rfq
    [Documentation]     Fill Rfq Panel and Send
    &{req}              Create Dictionary   fun=do_web_send_rfq  arg=   coh=   web=hang   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok

Coh: SellSide Reply
    [Documentation]     Accept RFQ
    &{req}              Create Dictionary   fun=do_coh_reply  arg=   coh=hang   web=none   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
    
Web: Manage Active Pane Rfq
    [Documentation]     Manage Active Rfq
    &{req}              Create Dictionary   fun=do_web_manage_rfq  arg=   coh=-   web=hang   timeout=120
    &{result}=          evaluate            test_cd_rfq.robot_run(&{req},'${cfg_file}')  
    ${info} =           Set Variable        ${result}[info]
    Should Be Equal As Strings              ${result}[status]     ok
