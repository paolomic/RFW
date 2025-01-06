
import sys
#from pathlib import Path

from datetime import datetime





checkval = r'C:\work\disks\D\wsp_c\127_28000.wsp4_wrk\Logs\MetaMarket_20250106.log'
COH_WSP=    r"C:\work\disks\D\wsp_c\127_28000.wsp4"

def get_today_iso():
  return datetime.now().strftime('%Y%m%d')

def get_log_path(wsp_path, logname):
  filename = f'{logname}_{get_today_iso()}.log'
  return f'{wsp_path}_wrk\\Logs\\{filename}'

log_path = get_log_path(COH_WSP, 'MetaMarket')
print (log_path)
print (log_path==checkval)



