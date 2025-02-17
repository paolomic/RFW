import multiprocessing
import time
import os

class TimeoutError(Exception):
    pass

# Funzione globale per eseguire la funzione target in un processo separato
def _run_function(queue, func, args, kwargs):
    try:
        result = func(*args, **kwargs)
        queue.put(result)
    except Exception as e:
        queue.put(e)

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
    # Creiamo una coda per comunicare il risultato
    queue = multiprocessing.Queue()

    # Creiamo un processo per eseguire la funzione
    process = multiprocessing.Process(
        target=_run_function,
        args=(queue, func, args, kwargs)
    )
    process.start()

    # Attendiamo che il processo termini entro il timeout
    process.join(seconds)

    # Se il processo è ancora attivo, significa che il timeout è scaduto
    if process.is_alive():
        process.terminate()
        process.join(timeout=1)  # Aspettiamo un po' per dare tempo al processo di terminare
        if process.is_alive():
            # Se il processo è ancora attivo, usiamo un metodo più aggressivo
            process.kill()
            process.join()
        raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")

    # Otteniamo il risultato dalla coda
    if not queue.empty():
        result = queue.get()
        if isinstance(result, Exception):
            raise result
        return result
    else:
        raise TimeoutError(f"Function {func.__name__} did not return any result")

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
        print(exec_intime(test1, 5))  # Timeout di 5 secondi
    except TimeoutError as e:
        print(e)
        os._exit(1)  # Termina immediatamente il processo corrente

    try:
        print(exec_intime(test2, 3))  # Timeout di 3 secondi
    except TimeoutError as e:
        print(e)
        os._exit(1)  # Termina immediatamente il processo corrente