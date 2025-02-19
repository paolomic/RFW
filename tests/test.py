import time
import random

class RetryContext:
    def __init__(self, max_seconds=10, interval=2, ignore_exceptions=False):
        self.max_seconds = max_seconds
        self.interval = interval
        self.ignore_exceptions = ignore_exceptions
    
    def __call__(self, func, *args, **kwargs):
        start_time = time.time()
        end_time = start_time + self.max_seconds
        attempts = 0
        
        # Primo tentativo
        try:
            attempts += 1
            print(f"Tentativo #{attempts}")
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except Exception as e:
            if not self.ignore_exceptions:
                print(f"Eccezione nel tentativo #{attempts}: {e} (non ignorata)")
                raise
            print(f"Eccezione nel tentativo #{attempts}: {e} (ignorata)")
            result = None
        
        # Tentativi successivi
        while time.time() < end_time:
            # Calcola il tempo rimanente
            remaining_time = end_time - time.time()
            
            # Determina se questo è l'ultimo tentativo possibile
            wait_time = min(self.interval, remaining_time)
            is_last_attempt = (remaining_time - wait_time) < self.interval
            
            # Attendi prima del prossimo tentativo
            if wait_time > 0:
                time.sleep(wait_time)
            
            # Esegui il tentativo
            try:
                attempts += 1
                print(f"Tentativo #{attempts}" + (" (ultimo)" if is_last_attempt else ""))
                result = func(*args, **kwargs)
                if result is not None:
                    return result
            except Exception as e:
                # Se è l'ultimo tentativo o non dobbiamo ignorare le eccezioni, propaghiamo l'errore
                if is_last_attempt or not self.ignore_exceptions:
                    print(f"Eccezione nel tentativo #{attempts}: {e} (non ignorata)")
                    raise
                print(f"Eccezione nel tentativo #{attempts}: {e} (ignorata)")
                result = None
        
        return None

def retry_for(max_seconds=10, interval=2, ignore_exceptions=False):
    """
    Wrapper per la funzione retry che accetta una funzione con i suoi argomenti.
    
    Args:
        max_seconds: Tempo massimo di attesa in secondi
        interval: Intervallo tra i tentativi in secondi
        ignore_exceptions: Se True, ignora le eccezioni durante i tentativi (tranne l'ultimo)
    """
    def wrapper(func, *args, **kwargs):
        context = RetryContext(max_seconds, interval, ignore_exceptions)
        return context(func, *args, **kwargs)
    return wrapper

if __name__ == '__main__':
    # Funzione di test che a volte ritorna None, a volte un valore, a volte solleva un'eccezione
    def test_function(x=5, y=5):
        r = random.random()
        
        if r < 0.3:  # 30% delle volte ritorna un valore
            result = x + y
            print(f"test_function: ritorna {result}")
            return result
        elif r < 0.7:  # 40% delle volte ritorna None
            print("test_function: ritorna None")
            return None
        else:  # 30% delle volte solleva un'eccezione
            print("test_function: solleva un'eccezione")
            raise ValueError("Simulazione di errore")
    
    print("\n--- Test con ignore_exceptions=False (default) ---")
    try:
        result = retry_for(8, 1)(test_function, 10, 20)
        print(f"Risultato finale: {result}")
    except Exception as e:
        print(f"Eccezione catturata: {e}")
    
    print("\n--- Test con ignore_exceptions=True ---")
    try:
        result = retry_for(8, 1, ignore_exceptions=True)(test_function, 10, 20)
        print(f"Risultato finale: {result}")
    except Exception as e:
        print(f"Eccezione catturata: {e}")