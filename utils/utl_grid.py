import keyboard
import keyboard.mouse
import time

import utl_win as uw


#############################################################
# Util  GridMng - My
#############################################################
#region

# ROBOT_CMD_GET_PROP result: [x_off=22    y_top=0 y_bot=19        y_mid=9 col_from=2      col_to=4]

def create_by_win(win_grid):
    res = uw.robot_send(win_grid.handle, uw.ROBOT_CMD_GET_HEADER, input_str="")
    #print(f'ROBOT_CMD_GET_HEADER result: [{res}]')                                 # <== Debug
    grid_mng = create_grid(win_grid, res) 
    res = uw.robot_send(win_grid.handle, uw.ROBOT_CMD_GET_PROP, input_str="")   
    #print(f'ROBOT_CMD_GET_PROP result: [{res}]')                                   # <== Debug
    grid_mng.set_props(res)
    return grid_mng

def import_rows(grid_mng, num, mode="row", home=True):
    uw.grid_select_rows(grid_mng.win_grid, num, mode=mode, home=home)
    rows = uw.win_copy_to_clip(wait_init=1)
    return grid_mng.add_rows(rows)

def scroll_home(grid_mng):
    res = uw.robot_send(grid_mng.win_grid.handle, uw.ROBOT_CMD_GET_COL_POINT, input_str="1\t1")
    # manca scroll verticale

def set_sort(grid_mng, key):
    grid = grid_mng.win_grid
    wtop = grid_mng.win_top

    def set_sort_segment(seg, asc):
        (x,y) = grid_mng.get_col_point(seg)
        uw.win_mouse_move(grid, x,y)
        keyboard.mouse.click('right')
        uw.popup_reply(wtop, 'Sort Ascending' if asc else 'Sort Descending')
        
    def set_sort_default():
        (x,y) = grid_mng.get_header_point()
        uw.win_mouse_move(grid, x,y)
        keyboard.mouse.click('right')
        uw.popup_reply(wtop, 'Sort Default', skip_disabled=1)        # se gia def is disabled

    if (key=='default'):
        set_sort_default()
    else:
        for segment in key:
            set_sort_segment(segment[0], segment[1]=='ASC')

#endregion
 
#############################################################
# Class GridMng - AI
#############################################################
#region
class GridMng:
    EMPTY = ''
    win_grid = None
    win_top = None
    
    def __init__(self, win_grid, nl='\r\n'):
        self.data = {
            "headers": [],
            "rows": []
        }
        self.col_xs = {}  # column x positions
        self.props = {}   # grid properties
        self.nl = nl      
        self.row_num = 0
        self.win_grid = win_grid
        self.win_top = uw.win_get_top(win_grid)
    
    def set_props(self, prop_str: str) -> None:
        """Set properties from 'key1=val1\tkey2=val2' string"""
        for prop in prop_str.split('\t'):
            if '=' in prop:
                key, val = prop.split('=', 1)
                self.props[key.strip()] = val.strip()
    
    def get_row_num(self) -> int:
        return self.row_num
    
    def get_prop(self, name: str) -> int:
        """Get property value by name"""
        return int(self.props.get(name))
    
    def get_col_point(self, header: str) -> int:
        """Get x coordinate for column"""
        return (self.col_xs.get(header), self.get_prop('y_mid') )
    
    def get_header_point(grid_mng):
        x = grid_mng.get_prop('x_off') + 10
        y = grid_mng.get_prop('y_mid')
        return (x,y)
    
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
    
    def search_first_match(self, search_criteria: dict) -> dict:
        invalid_headers = [h for h in search_criteria.keys() if h not in self.data["headers"]]
        if invalid_headers:
            raise ValueError(f"Headers non validi: {invalid_headers}")
            
        for row in self.data["rows"]:
            if all(row.get(header) == value for header, value in search_criteria.items()):
                return row
                
        return None
    
    def get_json(self) -> dict:
        """Get grid data and properties as dict"""
        return {
            "data": self.data,
            "props": self.props,
            "col_xs": self.col_xs
        }

def create_grid(win_grid, hdr_str: str, nl='\r\n') -> GridMng:
    """Create and initialize grid with headers"""
    grid = GridMng(win_grid, nl=nl)
    grid.set_headers(hdr_str)
    return grid

#endregion