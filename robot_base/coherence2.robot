*** Settings ***
Library    Process
Library    OperatingSystem
Library    WhiteLibrary

*** Variables ***
${APP_PATH}    D:\\COH_x64_CANDEAL_NEXT\\bin\\Coherence.exe    # Sostituisci con il percorso reale
${WINDOW_TITLE}    Starting Coherence.*    # Regexp per matchare qualsiasi versione

*** Test Cases ***
Launch And Click Open
    # Lancia l'applicazione
    Launch Application    ${APP_PATH}
    
    # Attende e attiva la finestra usando regexp
    Attach Window    ${WINDOW_TITLE}    regex=True
    
    # Cerca e preme il pulsante "Open"
    Click Button    Open
    
    [Teardown]    Close Application