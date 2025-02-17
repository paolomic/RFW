import time
import threading

def test1(arg):
    print('enter1')
    time.sleep(10)
    print('exit1')

def timeout_controller(timeout, action):
    time.sleep(timeout)
    action()

def robot_run(fun_name: str, arg: str, conn='', timeout=0):
    try:
        func = globals().get(fun_name)
        
        if timeout > 0:
            # Definisci l'azione da eseguire in caso di timeout
            def timeout_action():
                print(f"Timeout reached! Function {fun_name} took too long to execute.")
            
            # Crea e avvia il thread per il controllo del timeout
            timeout_thread = threading.Thread(target=timeout_controller, args=(timeout, timeout_action))
            timeout_thread.start()
        
        # Esegui la funzione principale nel thread principale
        result = func(arg)
        
        return result
    except Exception as e:
        excp = str(e)
        # Chiude processi (se necessario)
        print(f'exception {excp}')

if __name__ == '__main__':
    # Esecuzione dei test
    robot_run('test1', '', '', 5)  # Imposta un timeout di 5 secondi