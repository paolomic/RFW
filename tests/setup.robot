*** Settings ***
Documentation       Coherence Session Suite
Library             OperatingSystem
Library             Collections
Library             ../utils/test/test_setup.py  AS  test_new


*** Variables ***
&{opts}             repair=no  option2=value2


*** Test Cases ***
Start Setup
    [Documentation]     Setup run
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_setup.robot_run('do_setup','${arg}',${opts},'new')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok


Continue
    [Documentation]     Setup run
    [Timeout]           2 minutes
    ${arg}=             Set Variable  ${EMPTY}
    &{result}=          evaluate      test_setup.robot_run('do_go','${arg}',${opts},'hang')  
    log                               result: ${result}
    ${info} =           Set Variable  ${result}[info]
    Should Be Equal As Strings        ${result}[status]     ok

