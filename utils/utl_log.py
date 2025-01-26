import re
import json
from datetime import datetime, timedelta
from time import sleep
import utl  as utl
###################################
#Cappello


def GetLogRows(logpath, class_name, field_name, field_value, start_time, retry = 3, wait_s = 1):
    if (start_time=='now'):
        now = datetime.now()
        start_time = f'{now.hour:02}:{now.minute:02}:{now.second:02}'
    
    while retry > 0:
        result = _GetLogRows(logpath, class_name, field_name, field_value, start_time)
        if (result):
            return result
        sleep(wait_s)
        retry -= 1


###################################


def time_to_seconds(time_str):
    """
    Converte un timestamp HH:mm:ss in secondi dal mezzanotte.
    rrr
    Args:
    - time_str (str): Timestamp nel formato HH:mm:ss
    
    Returns:
    - int: Secondi trascorsi dal mezzanotte
    """
    t = datetime.strptime(time_str, "%H:%M:%S")
    return t.hour * 3600 + t.minute * 60 + t.second

def _GetLogRows(logpath, class_name, field_name, field_value, start_time):
    """
    Estrae l'ultima riga di log che corrisponde ai criteri specificati.
    
    Args:
    - logpath (str): Percorso del file di log
    - class_name (str): Nome della classe da cercare
    - field_name (str): Nome del campo da filtrare
    - field_value (str): Valore del campo da filtrare
    - start_time (str): Timestamp iniziale di ricerca nel formato HH:mm:ss
    
    Returns:
    - dict: Dizionario contenente le informazioni dell'ultima riga corrispondente
           o None se nessuna riga corrisponde
    """
    try:
        # Converte il tempo iniziale in secondi
        target_seconds = time_to_seconds(start_time)
        
        # Apre il file in modalità binaria
        with open(logpath, 'rb') as file:
            # Va alla fine del file
            file.seek(0, 2)
            
            # Inizia a leggere all'indietro
            block_size = 4096  # Dimensione del blocco di lettura
            block = b''
            lines = []
            
            while file.tell() > 0:
                # Determina quanto indietro spostarsi
                if file.tell() > block_size:
                    file.seek(-block_size, 1)
                else:
                    file.seek(0)
                
                # Leggi il blocco
                block = file.read(block_size) + block
                
                # Divide in righe
                lines = block.split(b'\n') + lines
                
                # Riposiziona il file
                file.seek(-len(block), 1)
                
                # Controlla le righe
                for line in reversed(lines):
                    try:
                        line_str = line.decode('utf-8', errors='ignore')
                        
                        # Estrai timestamp
                        timestamp_match = re.search(r'^(\d{2}:\d{2}:\d{2})\.\d{3}', line_str)
                        if not timestamp_match:
                            continue
                        
                        timestamp = timestamp_match.group(1)
                        line_seconds = time_to_seconds(timestamp)
                        
                        # Interrompi se il timestamp è precedente al target
                        if line_seconds < target_seconds:
                            return None
                        
                        # Verifica criteri di ricerca
                        if (class_name in line_str and 
                            f"{field_name}:({field_value})" in line_str):
                            
                            # Estrae tutti i campi
                            fields = {}
                            field_entries = re.findall(r'(\w+):\(([^)]*)\)', line_str)
                            for entry_name, entry_value in field_entries:
                                fields[entry_name] = entry_value
                            
                            # Restituisce l'ultima riga corrispondente
                            return {
                                'timestamp': timestamp,
                                'class_name': class_name,
                                'fields': fields
                            }
                    except Exception:
                        continue
                
                # Resetta le linee
                lines = []
        
        return None
    
    except FileNotFoundError:
        print(f"Errore: File {logpath} non trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return None

# Esempio di utilizzo
if __name__ == '__main__':
    import time
    
    start = time.time()
    result = GetLogRows(
        'C:\\Users\\Paolo.Michetti\\OneDrive - ION\\Desktop\\big.log', 
        'CLIENT_ORDER', 
        'ComplianceText', 
        'TEST_XXX',
        start_time='10:01:45'  # Cerca a partire da questo timestamp
    )
    end = time.time()
    
    print(f"Tempo di esecuzione: {end - start:.2f} secondi")
    
    if result:
        print(json.dumps(result, indent=2))