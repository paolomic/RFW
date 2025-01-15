class GridManager:
    def __init__(self, newline='\r\n'):
        self.data = {
            "headers": [],
            "rows": []
        }
        self.newline = newline
    

    def set_headers_from_string(self, header_string: str) -> None:
        """
        Imposta gli headers del grid da una stringa TAB-separated
        
        Args:
            header_string (str): Stringa con headers separati da tab
        """
        self.data["headers"] = [h.strip() for h in header_string.split('\t')]
    
    def _split_with_trailing_tabs(self, value_string: str) -> list:
        """
        Divide una stringa mantenendo i campi vuoti anche in coda,
        ignorando correttamente \r\n finali
        """
        # Rimuoviamo esplicitamente \r\n dalla fine
        value_string = value_string.rstrip('\r\n')
        
        # Split sulla stringa pulita
        values = value_string.split('\t')
        
        return values
    
    def add_row_from_string(self, value_string: str) -> dict:
        """
        Aggiunge una riga al grid da una stringa TAB-separated
        """
        # Split mantenendo i campi vuoti
        values = self._split_with_trailing_tabs(value_string)
        
        if len(values) != len(self.data["headers"]):
            raise ValueError(
                f"Il numero di valori ({len(values)}) non corrisponde al numero di headers ({len(self.data['headers'])}). " +
                f"Headers: {len(self.data['headers'])}, " +
                f"Values: {len(values)}"
            )
            
        # Crea il dizionario trattando le stringhe vuote come None
        row = {}
        for header, value in zip(self.data["headers"], values):
            value = value.strip()
            row[header] = value if value else None
            
        self.data["rows"].append(row)
        return row
        
    def add_rows_from_string(self, rows_string: str) -> list:
        """
        Aggiunge multiple righe al grid da una stringa con righe separate da newline
        """
        # Split sulle righe, rimuovendo righe vuote
        rows = [row for row in rows_string.split(self.newline) if row.strip()]
        added_rows = []
        
        for row_string in rows:
            try:
                row = self.add_row_from_string(row_string)
                added_rows.append(row)
            except ValueError as e:
                # Se c'è un errore in una riga, rimuovi le righe già aggiunte
                for _ in range(len(added_rows)):
                    self.data["rows"].pop()
                raise ValueError(f"Errore nella riga '{row_string}': {str(e)}")
                
        return added_rows
    
    def add_rows_from_string(self, rows_string: str) -> list:
        # Split sulle righe, mantenendo righe che potrebbero essere solo tab
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
                raise ValueError(f"Errore nella riga '{row_string}': {str(e)}")
                
        return added_rows
    
    def search_first_match(self, search_criteria: dict) -> dict:
        """
        Cerca il primo record che corrisponde ai criteri di ricerca specificati
        
        Args:
            search_criteria (dict): Dizionario con coppie header:value da cercare
            
        Returns:
            dict: Primo record che corrisponde ai criteri, None se non trovato
            
        Raises:
            ValueError: Se uno degli headers specificati non esiste nel grid
        """
        invalid_headers = [h for h in search_criteria.keys() if h not in self.data["headers"]]
        if invalid_headers:
            raise ValueError(f"Headers non validi: {invalid_headers}")
            
        for row in self.data["rows"]:
            if all(row.get(header) == value for header, value in search_criteria.items()):
                return row
                
        return None
    
    def get_json(self) -> dict:
        """
        Restituisce il grid completo come dizionario
        
        Returns:
            dict: Il grid completo
        """
        return self.data
    
    def clear(self) -> None:
        """Pulisce tutti i dati del grid mantenendo gli headers"""
        self.data["rows"] = []
        
    def get_row_count(self) -> int:
        """
        Restituisce il numero di righe nel grid
        
        Returns:
            int: Numero di righe
        """
        return len(self.data["rows"])

# Le funzioni helper rimangono invariate
def create_grid(header_string: str, newline='\r\n') -> GridManager:
    grid = GridManager(newline=newline)
    grid.set_headers_from_string(header_string)
    return grid

def add_grid_row(grid: GridManager, value_string: str) -> dict:
    return grid.add_row_from_string(value_string)

def add_grid_rows(grid: GridManager, rows_string: str) -> list:
    return grid.add_rows_from_string(rows_string)