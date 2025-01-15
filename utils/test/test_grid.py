


# import da altri path - MAMMAMIA :(
import sys
from pathlib import Path
_path_import = str(Path(__file__).parent.parent)
sys.path.append(_path_import) 

import utl_grid as ug

# Creiamo un grid con gli headers
s1 = "tipo\tstato"
grid = ug.create_grid(s1)  # Default newline='\r\n' per Windows

# Stringa con multiple righe (usando il newline di Windows \r\n)
rows = "Corporate bond\tNo\r\nCorporate bond\tNo\r\nCorporate bond\tNo\r\nCorporate bond\tNo\r\nCorporate bond\tNo"

# Aggiungiamo tutte le righe in una volta
added_rows = ug.add_grid_rows(grid, rows)
print(f"Aggiunte {len(added_rows)} righe")

# Verifichiamo il contenuto
print(grid.get_json())

s1 = "SecType\tSecurityRef"                 # get with keyword
ug.grid = ug.create_grid(s1) 
# Se volessimo usare un grid con newline Unix
#unix_grid = ug.create_grid(s1, newline='\n')