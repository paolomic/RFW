import time

class RetryContext:
    def __init__(self, timeout=10, delay=2, skip_excp=False):
        self.timeout = timeout
        self.delay = delay
        self.skip_excp = skip_excp
    
    def __call__(self, func):
        def wrapped(*args, _timeout=None, _delay=None, **kwargs):
 
            timeout = _timeout if _timeout is not None else self.timeout
            delay = _delay if _delay is not None else self.delay

            start_time = time.time()
            end_time = start_time + timeout
            attempt = 0

            while time.time() < end_time:
                attempt += 1
                is_last_attempt = time.time() + delay >= end_time

                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    if not self.skip_excp or is_last_attempt:
                        raise  # Solleva l'eccezione se skip_excp=False o è l'ultimo tentativo
                    print(f"Tentativo {attempt} fallito: {e}. Riprovo...")

                time.sleep(delay)
            
            return None
        return wrapped

def retry_for(timeout=10, delay=2, skip_excp=False):
    return RetryContext(timeout, delay, skip_excp)

if __name__ == '__main__':
    # Funzione originale
    def test2(x=5, y=5):
        # Simulazione: ritorna None le prime volte, poi un risultato, oppure solleva un'eccezione
        import random
        if random.random() < 0.0:
            raise ValueError("Errore casuale!")
        result = None
        if random.random() < 0.1:
            result = x + y
        print(f'test2 res: {result}')
        return result

    # Creazione della funzione derivata con ritentativi
    test2_retry = retry_for(timeout=10, delay=2, skip_excp=True)(test2)

    # Chiamata con valori predefiniti
    print("Chiamata con valori predefiniti:")
    try:
        result = test2_retry(x=7, _timeout=5, _delay=.5)
        print(f'Out res: {result}')
    except Exception as e:
        print(f'Errore finale: {e}')

   