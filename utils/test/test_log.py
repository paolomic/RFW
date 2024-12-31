import json

# import da altri path - 
import sys
from pathlib import Path
path_utl = str(Path(__file__).parent.parent)
sys.path.append(path_utl)

import utl_log


#'D:\\wsp_c\\127_28000.wsp4_wrk\\Logs\MetaMarket_20241218.log', 

result = utl_log.GetLogRows(
    'C:\\Users\\Paolo.Michetti\\OneDrive - ION\\Desktop\\big.log', 
    'CLIENT_ORDER', 
    'ComplianceText', 
    'TEST_XXX',
    start_time='16:00:00'
)

if result:
    timer = result['timestamp']
    OrderID = result['fields']['OrderID']
    print(f'Ho Trovato l\'ordine: [{OrderID}] delle ore {timer}')
    print(json.dumps(result, indent=2))
else:
    print('no such order!')