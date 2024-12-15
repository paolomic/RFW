*** Settings ***
Library    Process
Library    OperatingSystem
Library    AutoItLibrary

*** Variables ***
${APP_PATH}    D:\\COH_x64_CANDEAL_NEXT\\bin\\Coherence.exe
${WINDOW_TITLE}    Starting Coherence [DEBUG version]

*** Test Cases ***
Launch And Click Open
    # Lancia l'applicazione
    Start Process    ${APP_PATH}    alias=coherence
    Sleep    3s    # Aspetta che l'app si avvii
    
    # Verifica se la finestra esiste
    ${window_exists}=    Win Exists    ${WINDOW_TITLE}    
    Log    Window exists: ${window_exists}
    
    # Se la finestra esiste, prova ad attivarla e cliccare
    Run Keyword If    ${window_exists}    Continue Test
    ...    ELSE    Fail    Window not found!

    [Teardown]    Terminate Application

*** Keywords ***
Continue Test
    Win Activate    ${WINDOW_TITLE}
    Sleep    1s
    Control Click    ${WINDOW_TITLE}  ${EMPTY}  [CLASS:Button;TEXT:Open]
    Sleep    1

Terminate Application
    Terminate Process    coherence    kill=True