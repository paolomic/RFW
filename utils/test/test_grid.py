


# import da altri path - MAMMAMIA :(
import sys
from pathlib import Path
_path_import = str(Path(__file__).parent.parent)
sys.path.append(_path_import) 

import utl_grid as ug

# Test con il codice corretto
grid = ug.create_grid("nome,(1,2)\tcognome,(3,4)\tetà")

print("Test completo degli headers:")
for i in range(len(grid.data["headers"])):
    name = grid.get_header_name(i)
    point = grid.get_header_point(i)
    print(f"Header {i}: {name} -> Point: {point}")

# Aggiungiamo una riga per verificare che tutto funzioni
ug.add_grid_row(grid, "Mario\tRossi\t30")

print("\nJSON completo:")
print(grid.get_json())