*** Settings ***
Documentation       CanDeal BuySide -  Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_cd_buyside.py  AS  test_cd_buyside


*** Variables ***
&{opts}             speed=110    run=local    reuse_wsp=yes  save_wsp_onclose=yes  close_all_pages=yes                                                    # list of Suite Options
#@{addin_list}       MetaMarket  UserPages
&{req_dict}         path=http://10.91.204.20/login    title=Chrome
${ftqid}            000000000000


*** Test Cases ***
Start New Session
    [Documentation]     login
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_new.robot_run('do_login_session','${arg}',${opts},'new')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok
    