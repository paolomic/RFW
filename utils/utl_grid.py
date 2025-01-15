class GridManager:
    def __init__(self, newline='\r\n'):
        self.data = {
            "headers": [],
            "rows": []
        }
        self.newline = newline
        self._row_counter = 0  # Counter for row numbering
    
    def set_headers_from_string(self, header_string: str) -> None:
        """
        Imposta gli headers del grid da una stringa TAB-separated, aggiungendo 'nRow' come prima colonna
        
        Args:
            header_string (str): Stringa con headers separati da tab
        """
        # Add 'nRow' as first column
        headers = ['nRow'] + [h.strip() for h in header_string.split('\t')]
        self.data["headers"] = headers
    
    def _split_with_trailing_tabs(self, value_string: str) -> list:
        """
        Divide una stringa mantenendo i campi vuoti anche in coda,
        ignorando correttamente \r\n finali
        """
        value_string = value_string.rstrip('\r\n')
        return value_string.split('\t')
    
    def add_row_from_string(self, value_string: str) -> dict:
        """
        Aggiunge una riga al grid da una stringa TAB-separated,
        aggiungendo automaticamente il numero progressivo della riga
        """
        values = self._split_with_trailing_tabs(value_string)
        
        # Check length against expected headers (excluding 'nRow' which we'll add)
        if len(values) != len(self.data["headers"]) - 1:  # -1 because 'nRow' is extra
            raise ValueError(
                f"Il numero di valori ({len(values)}) non corrisponde al numero di headers ({len(self.data['headers']) - 1}). " +
                f"Headers: {len(self.data['headers']) - 1}, " +
                f"Values: {len(values)}"
            )
        
        # Increment row counter
        self._row_counter += 1
        
        # Create row dictionary with row number
        row = {'nRow': str(self._row_counter)}  # Convert to string to maintain consistency
        
        # Add the rest of the values
        for header, value in zip(self.data["headers"][1:], values):  # Skip 'nRow' header
            value = value.strip()
            row[header] = value if value else ''    # Void Input map to None or ''
            
        self.data["rows"].append(row)
        return row
    
    def add_rows_from_string(self, rows_string: str) -> list:
        """
        Aggiunge multiple righe al grid da una stringa con righe separate da newline
        """
        rows = [row for row in rows_string.split(self.newline) if row]
        added_rows = []
        
        for row_string in rows:
            try:
                row = self.add_row_from_string(row_string)
                added_rows.append(row)
            except ValueError as e:
                # Se c'è un errore in una riga, rimuovi le righe già aggiunte
                for _ in range(len(added_rows)):
                    self.data["rows"].pop()
                    self._row_counter -= 1  # Decrement counter for removed rows
                raise ValueError(f"Errore nella riga '{row_string}': {str(e)}")
                
        return self.get_row_count()
    
    def clear(self) -> None:
        """Pulisce tutti i dati del grid mantenendo gli headers e resettando il contatore righe"""
        self.data["rows"] = []
        self._row_counter = 0  # Reset row counter
    
    # Altri metodi rimangono invariati
    def search_first_match(self, search_criteria: dict) -> dict:
        invalid_headers = [h for h in search_criteria.keys() if h not in self.data["headers"]]
        if invalid_headers:
            raise ValueError(f"Headers non validi: {invalid_headers}")
            
        for row in self.data["rows"]:
            if all(row.get(header) == value for header, value in search_criteria.items()):
                return row
                
        return None
    
    def get_json(self) -> dict:
        return self.data
    
    def get_row_count(self) -> int:
        return len(self.data["rows"])

# Helper functions
def create_grid(header_string: str, newline='\r\n') -> GridManager:
    grid = GridManager(newline=newline)
    grid.set_headers_from_string(header_string)
    return grid

def add_grid_row(grid: GridManager, value_string: str) -> dict:
    return grid.add_row_from_string(value_string)

def add_grid_rows(grid: GridManager, rows_string: str) -> list:
    return grid.add_rows_from_string(rows_string)