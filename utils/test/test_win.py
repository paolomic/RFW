
# import da altri path - MAMMAMIA :(
import sys
from pathlib import Path
_path_import = str(Path(__file__).parent.parent)
sys.path.append(_path_import) 

import utl_win as uw



wnd = uw.find_window(name="Google Chrome - Paolo", exact_match=False)
print (wnd)

uw.win_activate(wnd)

#cld = uw.get_child(wnd, name='.*pieghevole.*', recursive=True,use_regex=True)
#print (cld)

cld = uw.get_child(wnd, ctrl_type='Pane', recursive=False)
print (cld)

cld = uw.get_child(cld, name='.*pieghevole.*', recursive=True,use_regex=True)
print (cld)


uw.win_clickon(cld)


