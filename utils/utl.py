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
# function retry #1

#sample:   
#    result = retry_for(8, 1)(test, 10, 20)    # chiama la test coi suoi arg ripetutamente

class RetryContext:
    def __init__(self, timeout=10, delay=2, skip_excp=False):
        self.timeout = timeout
        self.delay = delay
        self.skip_excp = skip_excp
    
    def __call__(self, func, *args, **kwargs):
        start_time = time.time()
        end_time = start_time + self.timeout
        attempts = 0
        
        # Primo tentativo
        try:
            attempts += 1
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except Exception as e:
            if not self.skip_excp:
                raise
            result = None
        
        while time.time() < end_time:
            remaining_time = end_time - time.time()
            wait_time = min(self.delay, remaining_time)
            is_last_attempt = (remaining_time - wait_time) < self.delay
            if wait_time > 0:
                time.sleep(wait_time)
            try:
                attempts += 1
                result = func(*args, **kwargs)
                if result is not None:
                    return result
            except Exception as e:
                if is_last_attempt or not self.skip_excp:
                    raise
                result = None
        return None

def retry_for(max_seconds=10, interval=2, ignore_exceptions=False):
    def wrapper(func, *args, **kwargs):
        context = RetryContext(max_seconds, interval, ignore_exceptions)
        return context(func, *args, **kwargs)
    return wrapper


#####################################################################
# function retry #2

#sample:
#   test_retry = retry_fun(_timeout=10, retry_delay=2, skip_excp=True, wait_init=0.25, wait_end=0.25)(test)   
# difinisce test_retry analoga a test, con in piu 5 arg cutomizabili


class RetryContext:
    def __init__(self, retry_timeout=10, retry_delay=2, skip_excp=False, wait_init=0.25, wait_end=0.25):
        self.timeout = retry_timeout
        self.delay = retry_delay
        self.skip_excp = skip_excp
        self.wait_init = wait_init
        self.wait_end = wait_end
    
    def __call__(self, func):
        def wrapped(*args, retry_timeout=None, retry_delay=None, **kwargs):
            timeout = retry_timeout if retry_timeout is not None else self.timeout
            delay = retry_delay if retry_delay is not None else self.delay

            time.sleep(self.wait_init)
            start_time = time.time()
            end_time = start_time + timeout
            attempt = 0

            while True:
                attempt += 1
                is_last_attempt = time.time() + delay >= end_time           # or timeout==0
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        time.sleep(self.wait_end)
                        return result
                except Exception as e:
                    if not self.skip_excp or is_last_attempt:
                        raise
                if is_last_attempt:
                    print(f'Exit Fail: retry_fun: attempt {attempt} ')
                    break
                time.sleep(delay)
            return None
        return wrapped

def retry_fun(retry_timeout=10, retry_delay=2, skip_excp=False, wait_init=0.25, wait_end=0.25):
    return RetryContext(retry_timeout, retry_delay, skip_excp, wait_init, wait_end)

