import threading
import time
import os

class TimeoutError(Exception):
    pass

def exec_intime(func, seconds, *args, **kwargs):
    """
    Esegue una funzione con un timeout specificato.

    :param func: La funzione da eseguire.
    :param seconds: Il timeout in secondi.
    :param args: Argomenti posizionali da passare alla funzione.
    :param kwargs: Argomenti keyword da passare alla funzione.
    :return: Il risultato della funzione se completata in tempo.
    :raises TimeoutError: Se la funzione non completa entro il timeout.
    """
    # Variabile per memorizzare il risultato della funzione
    result = None
    exception = None

    # Funzione che esegue la funzione target
    def target():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    # Creiamo un thread per eseguire la funzione
    thread = threading.Thread(target=target)
    thread.start()

    # Attendiamo che il thread termini entro il timeout
    thread.join(seconds)

    # Se il thread è ancora attivo, significa che il timeout è scaduto
    if thread.is_alive():
        # Interrompiamo il thread (non è sempre affidabile, ma è l'unica opzione)
        thread.join(timeout=0.1)  # Aspettiamo un po' per dare tempo al thread di terminare
        raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

    # Se c'è un'eccezione, la rilanciamo
    if exception is not None:
        raise exception

    return result

# Esempio di utilizzo della funzione
def test1():
    time.sleep(10)  # Simula un'operazione che richiede molto tempo
    print("Test1 completato")
    return "Successo test1"

def test2():
    time.sleep(1)  # Simula un'operazione che richiede poco tempo
    print("Test2 completato")
    return "Successo test2"





if __name__ == '__main__':
    # Esecuzione dei test
    try:
        print(exec_intime(test1, 5), flush=1)  # Timeout di 5 secondi
    except TimeoutError as e:
        print(e)
        os._exit(1)

    #try:
    #    print(exec_intime(test2, 3))  # Timeout di 3 secondi
    #except TimeoutError as e:
    #    print(e)
