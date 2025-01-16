class GridMng:
    EMPTY = ''
    
    def __init__(self, nl='\r\n'):
        self.data = {
            "headers": [],
            "rows": []
        }
        self.points = {}  # header coordinates
        self.props = {}   # grid properties
        self.nl = nl      
        self.row_num = 0
    
    def set_props(self, prop_str: str) -> None:
        """Set properties from 'key1=val1\tkey2=val2' string"""
        for prop in prop_str.split('\t'):
            if '=' in prop:
                key, val = prop.split('=', 1)
                self.props[key.strip()] = val.strip()
    
    def get_prop(self, name: str) -> str:
        """Get property value by name"""
        return self.props.get(name)
    
    def get_point(self, header: str) -> tuple:
        """Get coordinates (x,y) for header"""
        return self.points.get(header)
    
    def get_props(self) -> dict:
        """Get all properties"""
        return self.props.copy()
    
    def get_points(self) -> dict:
        """Get all header coordinates"""
        return self.points.copy()
    
    def set_headers(self, hdr_str: str) -> None:
        hdrs = ['nRow']
        self.points = {'nRow': None}
        
        for hdr_item in hdr_str.split('\t'):
            name, point = self._parse_header_coords(hdr_item)
            hdrs.append(name)
            self.points[name] = point
            
        self.data["headers"] = hdrs
    
    def _parse_header_coords(self, hdr_str: str) -> tuple:
        import re
        
        hdr_str = hdr_str.strip()
        match = re.match(r'^(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\)$', hdr_str)
        
        if match:
            name = match.group(1).strip()
            try:
                x = int(match.group(2))
                y = int(match.group(3))
                return name, (x, y)
            except ValueError:
                return hdr_str, None
        return hdr_str, None
    
    def add_row(self, val_str: str) -> dict:
        vals = val_str.rstrip(self.nl).split('\t')
        
        if len(vals) != len(self.data["headers"]) - 1:
            raise ValueError("Values count doesn't match headers count")
        
        self.row_num += 1
        row = {'nRow': str(self.row_num)}
        
        for hdr, val in zip(self.data["headers"][1:], vals):
            row[hdr] = val.strip() or self.EMPTY
            
        self.data["rows"].append(row)
        return row
    
    def add_rows(self, rows_str: str) -> list:
        rows = [row for row in rows_str.split(self.nl) if row]
        added = []
        
        for row_str in rows:
            try:
                row = self.add_row(row_str)
                added.append(row)
            except ValueError as e:
                for _ in range(len(added)):
                    self.data["rows"].pop()
                    self.row_num -= 1
                raise ValueError(f"Error in row '{row_str}': {str(e)}")
                
        return added
    
    def get_json(self) -> dict:
        """Get grid data and properties as dict"""
        return {
            "data": self.data,
            "props": self.props
        }

def create_grid(hdr_str: str, nl='\r\n') -> GridMng:
    """Create and initialize grid with headers"""
    grid = GridMng(nl=nl)
    grid.set_headers(hdr_str)
    return grid