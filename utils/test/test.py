import time
from contextlib import contextmanager


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

""" 
@contextmanager
def retry_function(max_seconds=10, interval=2):
    context = RetryContext(max_seconds, interval)
    try:
        yield context
    finally:
        pass  # Cleanup se necessario 
"""

# Esempio di utilizzo
def test2(x=4, y=7):
    # Simulazione: ritorna None le prime volte, poi un risultato
    import random
    result = None
    if random.random() < 0.1:
        result  = x+y
    print(f'Result {result}')
    return result

# Utilizzo simile alla sintassi richiesta
#with retry_function(max_seconds=10, interval=2) as retry:
#    result = retry(test2, 10, 11)

# Alternativa più compatta
def retry_for(max_seconds=10, interval=2):
    """Wrapper per la funzione retry che accetta una funzione con i suoi argomenti"""
    def wrapper(func, *args, **kwargs):
        context = RetryContext(max_seconds, interval)
        return context(func, *args, **kwargs)
    return wrapper



if __name__ == '__main__':
    result = retry_for(10, 2) (test2, y=11)
    print(f'Final Result {result}')