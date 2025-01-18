import utl_win as uw

#
# ROBOT_CMD_GET_PROP result: [x_off=22    y_top=0 y_bot=19        y_mid=9 col_from=2      col_to=4]


#############################################################
# GridMng AI
#############################################################
class GridMng:
    EMPTY = ''
    
    def __init__(self, nl='\r\n'):
        self.data = {
            "headers": [],
            "rows": []
        }
        self.col_xs = {}  # column x positions
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
    
    def get_col_point(self, header: str) -> int:
        """Get x coordinate for column"""
        return (self.col_xs.get(header), self.get_prop('y_mid') )
    
    def set_headers(self, hdr_str: str) -> None:
        """Set headers from 'name,x\tname2,x2' string. X coordinate is optional"""
        hdrs = ['nRow']
        self.col_xs = {'nRow': None}
        
        for hdr_item in hdr_str.split('\t'):
            name, x = self._parse_header_x(hdr_item)
            hdrs.append(name)
            self.col_xs[name] = x
            
        self.data["headers"] = hdrs
    
    def _parse_header_x(self, hdr_str: str) -> tuple:
        """Parse 'name,x' string. Returns (name, x) where x can be None"""
        parts = hdr_str.strip().split(',', 1)
        name = parts[0].strip()
        
        if len(parts) > 1:
            try:
                x = int(parts[1].strip())
                return name, x
            except ValueError:
                return name, None
        return name, None
    
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
            "props": self.props,
            "col_xs": self.col_xs
        }

def create_grid(hdr_str: str, nl='\r\n') -> GridMng:
    """Create and initialize grid with headers"""
    grid = GridMng(nl=nl)
    grid.set_headers(hdr_str)
    return grid

def create_by_win(win_grid) -> GridMng:
    grid = GridMng()
    res = uw.robot_send(win_grid.handle, uw.ROBOT_CMD_GET_HEADER, input_str="")
    #print(f'ROBOT_CMD_GET_HEADER result: [{res}]')                                 # <== Debug
    jsgrid = create_grid(res) 
    res = uw.robot_send(win_grid.handle, uw.ROBOT_CMD_GET_PROP, input_str="")   
    #print(f'ROBOT_CMD_GET_PROP result: [{res}]')                                   # <== Debug
    jsgrid.set_props(res)
    return jsgrid