from datetime import datetime, timedelta
import time
from functools import wraps
import winsound

def get_now_sec(sep=':'):
    now = datetime.now()
    return f'{now.hour:02}{sep}{now.minute:02}{sep}{now.second:02}'

def play_sound(type):
    if type=='success':
        #winsound.Beep(1000, 100)
        #winsound.Beep(1000, 100)
        wav_file = r"C:\Windows\Media\Windows Print complete.wav"
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)
    elif type=='fail':
        #winsound.Beep(200, 1000)
        wav_file = r"C:\Windows\Media\Windows Critical Stop.wav"
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)


def chrono(func):                  # Analisi: set as Decorator: @....
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Funzione {func.__name__} eseguita in {execution_time:.2f} ms")
        return result
    return wrapper


class TimeOut():
    timeout = 120
    start_time = 0
    def __init__(self, timeout):
        self.set(timeout)
        self.reset()
    def set(self, timeout):
        self.timeout = timeout
    def reset(self):
        self.start_time = time.time()
    def expired(self):
        return time.time() - self.start_time > self.timeout


def get_conn_events(input_string, phase_type: str) -> list:
    try:
        parts = input_string.split()
        phase_dict = {}
        
        for part in parts:
            key, values = part.split(':')
            phase_dict[key] = values.split(',')
        return phase_dict.get(phase_type, [])
    except:
        return None

def sleep_progress(sec):
    to = TimeOut(sec)
    while not to.expired():
        print('.', end='', flush=1)
        time.sleep(1)
    print('')

#####################################################################
# timeout execution
import threading

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


#####################################################################
# timeout execution - METOTODO 2 dovrebbe interrompere ip rocesso child


import multiprocessing


class TimeoutError(Exception):
    pass

# Funzione globale per eseguire la funzione target in un processo separato
def _run_function(queue, func, args, kwargs):
    try:
        result = func(*args, **kwargs)
        queue.put(result)
    except Exception as e:
        queue.put(e)

def exec_intime_2(func, seconds, *args, **kwargs):
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
        # Terminiamo il processo in modo forzato
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






if __name__ == '__main__':
    play_sound('fail')
    sleep_progress(4)