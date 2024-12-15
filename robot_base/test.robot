*** Settings ***
Documentation    Simple Calculator Test
Library          OperatingSystem
Library          Collections
Library          utils.py


*** Test Cases ***
Addition Test
   [Documentation]    Test the addition operation of the calculator
   ${expression}    Set Variable    2 + 3
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    5


Subtraction Test
   [Documentation]    Test the subtraction operation of the calculator
   ${expression}    Set Variable    5 - 2
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    3


Multiplication Test
   [Documentation]    Test the multiplication operation of the calculator
   ${expression}    Set Variable    4 * 3
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    12


Division Test
   [Documentation]  Test the division operation of the calculator
   ${expression}   Set Variable    25 / 5
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers   ${result}    5


Module Test
   [Documentation]  Test the Module operation of the calculator
   ${expression}   Set Variable    50 % 5
   ${result}    Evaluate    ${expression}
   Should Be Equal As Numbers    ${result}    0

Example Test Case
   [Documentation]    Example of for loop and if condition
   [Tags]    example
   ${numbers}=    Set Variable    1    2    3    4    5  # Or you can use "Evaluate    [1, 2, 3, 4, 5]"
   ${sum}=    Set Variable    0
   FOR    ${number}    IN    @{numbers}
       Log    Number: ${number}
       ${sum}=    Evaluate    ${sum} + ${number}
   END
   Log    Total Sum: ${sum}
   IF    ${sum} > 10
       Log    Sum is greater than 10
   ELSE
       Log    Sum is not greater than 10
   END
   Should Be Equal As Numbers    ${sum}    15

External Python Test
    [Documentation]    Example how call external testting
    ${arg}=    Set Variable    capper
    ${result}=  evaluate    utils.test_dialog('${arg}')    modules=utils
    log  result: ${result}
    Should Be Equal As Strings    ${result}    ""