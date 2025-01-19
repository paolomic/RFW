*** Settings ***
Documentation    Simple Collection Tests
Library          OperatingSystem
Library          Collections
Library          test.py
Library         ../utils/test/test_coh.py    AS    test_coh


*** Test Cases ***
Addition Test
   [Documentation]    Algebric Addition Sample
   ${expression}    Set Variable    2 + 3
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    5

External Python Test
    [Documentation]    External Python Function Sample
    ${arg}=    Set Variable    cappero
    ${result}=  evaluate    test.test_dialog('${arg}')    modules=test
    log  result: ${result}
    Should Be Equal As Strings    ${result}    ok
    
Coherence Session - Send Care Order
    [Documentation]    Start Coherence Session, Send Care Order, Retrieve Order in Page
    [Timeout]    5 minutes    
    ${arg}=    Set Variable    1, 2, 3, prova
    ${result}=  evaluate    test_coh.robot_test('${arg}')    modules=test_coh
    log  result: ${result}
    Should Be Equal As Strings    ${result}    ok