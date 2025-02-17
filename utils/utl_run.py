
from utl_config import config
from utl_win import sleep, ROBOT_RES
from utl_verifier import VERIFY, RAISE, DUMP

from utl_app import app, Settings, BondDlg
from utl_web import wapp, WebTable, WebBondDlg

import utl as utl

####################################################################
#region - Util

def terminate_sessions():
    app.manage_conn('terminate', 'coh:all')
    wapp.manage_conn('terminate', 'web:all')

#endregion


####################################################################
#region - Base Mode: Simple Execution

def robot_run(func: callable, arg:str, cfg_file, conn='', timeout=0):
    def manage_conn(event):
        app.manage_conn(event, conn)
        wapp.manage_conn(event, conn)
    try:
        config.load(cfg_file)
        manage_conn('start')
        result = func(arg)
        manage_conn('exit')
        return ROBOT_RES('ok', result)
    except Exception as e:
        excp = str(e)
        DUMP(excp)

#endregion

####################################################################
#region - Mode 1: Execution in child Thread 

import threading

class TimeoutError(Exception):
    pass

exec_intime_tag = 'Robot_Call_Timeout'

def exec_intime(seconds, func, *args, **kwargs):
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
        raise TimeoutError(f"{exec_intime_tag}: Function {func.__name__} after {seconds} seconds")

    # Se c'è un'eccezione, la rilanciamo
    if exception is not None:
        raise exception

    return result



def robot_run_1(func:callable, arg:str, cfg_file, conn='', timeout=0):
    def manage_conn(event):
        app.manage_conn(event, conn)
        wapp.manage_conn(event, conn)
    try:
        config.load(cfg_file)
        manage_conn('start')
        if timeout:
            result = utl.exec_intime(timeout, func, arg)            # forked execution - time check - to test
        else:
            result = func(arg)
        manage_conn('exit')
        return ROBOT_RES('ok', result)
    except Exception as e:
        excp = str(e)
        DUMP(excp)
        if timeout and utl.exec_intime_tag in excp:
            manage_conn('terminate')                                  # chiude processi 

#endregion

####################################################################
#region - Mode 2: Timeout Controller in Child Thread

RS_NONE =       'none'
RS_START =      'start'
RS_DONE =       'done'      # execution completed, ok or no
RS_TIMEOUT =    'timeout'   # execution over timeout interrupted


class RunState:
    def __init__(self):
        self._run_state = RS_NONE
        self._lock = threading.Lock()       # ME

    def set(self, state):
        with self._lock:
            self._run_state = state

    def get(self):
        with self._lock:
            return self._run_state

run_state = RunState()
    
def timeout_controller(timeout):
    to = utl.TimeOut(timeout)
    while not to.expired():
         sleep(0.250)
         if run_state.get()==RS_DONE:
            return
    if run_state.get() != RS_DONE:
        print('Test Execution Timeout')
        run_state.set(RS_TIMEOUT)
        terminate_sessions()

def start_controller(timeout):
    if not timeout:
        return None
    timeout_thread = threading.Thread(target=timeout_controller, args=(timeout,))
    timeout_thread.start()
    #stop_event = threading.Event()
    return timeout_thread

def end_controller(timeout, timeout_thread):
    if not timeout:
        return None
    #timeout_thread.join() 

def robot_run_2(func:callable, arg:str, cfg_file, conn='', timeout=0):
    def manage_conn(event):
        app.manage_conn(event, conn)
        wapp.manage_conn(event, conn)
    try:
        run_state.set(RS_START)
        config.load(cfg_file)
        manage_conn('start')
        timeout_thread  = start_controller(timeout)
        result = func(arg)
        manage_conn('exit')
        #end_controller(timeout, timeout_thread )
        if (run_state.get()==RS_TIMEOUT):        
            RAISE('Test Execution takes more than {timeout} seconds.')
        else:
            run_state.set(RS_DONE)
        
        return ROBOT_RES('ok', result)
    except Exception as e:
        excp = str(e)
        #print (f'runstate {run_state.get()}')
        if (run_state.get()==RS_TIMEOUT):
            excp = 'Test Timeout Detected - Process Interrupted: ' + excp
        DUMP(excp)


#endregion