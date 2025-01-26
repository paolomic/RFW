from datetime import datetime, timedelta
from time import sleep

def get_now_sec(sep=':'):
    now = datetime.now()
    return f'{now.hour:02}{sep}{now.minute:02}{sep}{now.second:02}'
