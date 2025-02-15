
import time

# Import 
import sys
from pathlib import Path
_new_path = str(Path(__file__).parent.parent)
sys.path.append(_new_path) 

import utl  as utl

class TimeOut():
    timeout = 120
    start_time = 0
    def __init__(self, timeout):
        self.timeout = timeout
        self.start_time = time.time()
    def expired(self):
        return time.time() - self.start_time > self.timeout


while TimeOut(3):
    print(1)
    time.sleep(1)