import multiprocessing
import time
import os

def test1(arg):
    print('enter1')
    time.sleep(10)  # Simula un'operazione lunga
    print('exit1')

def test2(arg):
    print('enter2')
    time.sleep(5)  # Simula un'operazione lunga
    print('exit2')

def target(queue, func, arg):
    """Funzione eseguita nel processo figlio."""
    try:
        result = func(arg)
        queue.put((True, result))
    except Exception as e:
        queue.put((False, str(e)))

def run_with_timeout(func, arg, timeout):
    """Esegue la funzione in un processo separato con un timeout."""
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=target, args=(queue, func, arg))
    process.start()
    process.join(timeout)  # Attende il timeout

    if process.is_alive():
        # Se il processo è ancora in esecuzione, termina forzatamente
        process.terminate()
        process.join()
        raise TimeoutError(f"Timeout: la funzione '{func.__name__}' ha superato il tempo massimo di {timeout} secondi")
    else:
        # Se il processo è terminato, recupera il risultato
        if not queue.empty():
            success, result = queue.get()
            if success:
                return result
            else:
                raise Exception(result)
        else:
            raise Exception("Errore: nessun risultato disponibile")

def robot_run(fun_name: str, arg: str, conn='', timeout=0):
    try:
        func = globals().get(fun_name)
        if not func:
            raise ValueError(f"Funzione '{fun_name}' non trovata.")

        if timeout > 0:
            result = run_with_timeout(func, arg, timeout)
        else:
            result = func(arg)
        return result
    except Exception as e:
        excp = str(e)
        print(f'exception {excp}')

if __name__ == '__main__':
    # Esecuzione dei test
    try:
        print("Esecuzione di test1 con timeout di 3 secondi:")
        robot_run('test1', '', '', 3)  # Timeout di 3 secondi
    except Exception as e:
        print(e)

    try:
        print("\nEsecuzione di test2 con timeout di 3 secondi:")
        robot_run('test2', '', '', 3)  # Timeout di 3 secondi
    except Exception as e:
        print(e)