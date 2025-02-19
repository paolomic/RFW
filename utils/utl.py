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
        return self.elapsed() > self.timeout
    def elapsed(self):
         return time.time() - self.start_time


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
# process kill forced

import ctypes
import ctypes.wintypes
import win32process

def win_get_pid(win):
    return win32process.GetWindowThreadProcessId(win.handle)[1]

def process_kill(win='', pid=None):
    #pid = win.ProcessId  # Ottieni il PID dalla finestra
    if not pid:
        pid = win_get_pid(win)
    print(f'Terminanting WND {win} {win.handle}')
    print(f'Terminanting PID {pid}')
    # Apri il processo con permessi di terminazione
    PROCESS_TERMINATE = 0x0001
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
    if not handle:
        raise ctypes.WinError()  # Solleva un'eccezione se l'apertura fallisce
    # Termina il processo
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.CloseHandle(handle)  # Chiudi l'handle del processo
    print(f"process kill Done")



#####################################################################
# function retry

class RetryContext:
    def __init__(self, max_seconds=10, interval=2):
        self.max_seconds = max_seconds
        self.interval = interval
    
    def __call__(self, func, *args, **kwargs):
        start_time = time.time()
        end_time = start_time + self.max_seconds
        
        result = func(*args, **kwargs)
        if result is not None:
            return result
            
        while time.time() < end_time:
            time.sleep(self.interval)
            result = func(*args, **kwargs)
            if result is not None:
                return result
        
        return None

def retry_for(max_seconds=10, interval=2):
    def wrapper(func, *args, **kwargs):
        context = RetryContext(max_seconds, interval)
        return context(func, *args, **kwargs)
    return wrapper

if __name__ == '__main__':
    def test2(x=5, y=5):
        # Simulazione: ritorna None le prime volte, poi un risultato
        import random
        result = None
        if random.random() < 0.1:
            result  = x+y
        print(f'test2 res: {result}')
        return result

    result = retry_for(10, 2) (test2)
    print(f'Out res: {result}')