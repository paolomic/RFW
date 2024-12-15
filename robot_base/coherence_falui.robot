*** Settings ***
Library    FlaUILibrary
Library    Process
Library    OperatingSystem

*** Variables ***
${APP_PATH}        D:\\COH_x64_CANDEAL_NEXT\\bin\\Coherence.exe
${WINDOW_TITLE}    Starting Coherence [DEBUG version]

*** Test Cases ***
Launch And Click Open
    # Lancia l'applicazione
    Start Process    ${APP_PATH}    alias=coherence
    
    # Attende che la finestra principale sia visibile (timeout di 10 secondi)
    Wait Until Element Is Visible    name:${WINDOW_TITLE}    timeout=10
    
    # Cerca e preme il pulsante "Open"
    Click    name:Open
    
    # Opzionale: verifica che il pulsante sia stato premuto correttamente
    # Qui puoi aggiungere verifiche specifiche in base al comportamento atteso
    
    [Teardown]    Terminate Application

*** Keywords ***
Terminate Application
    Terminate Process    alias=coherence    kill=True