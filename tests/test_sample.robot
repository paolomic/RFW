*** Settings ***
Documentation    Simple Collection Tests
Library          OperatingSystem
Library          Collections
Library          test.py


*** Test Cases ***
Addition Test
   [Documentation]    Algebric Addition Sample
   ${expression}    Set Variable    2 + 3
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    5

External Python Test
    [Documentation]    External Python Function Sample
    ${arg}=    Set Variable    cappero
    &{result}=  evaluate    test.test_dialog('${arg}')    modules=test
    log  object_res: ${result}
    ${status}=  evaluate      $result.status
    ${data}=  evaluate      $result.data
    ${info}=  evaluate      $result.info
    log  ${status}
    log  ${data}
    log  ${info}
    Should Be Equal As Strings    ${status}    ok
    


*** Keywords ***
My Log
    [Arguments]    ${expression}    ${expected}
    Log           C${expression}=