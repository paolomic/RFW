from win32api import GetFileVersionInfo, LOWORD, HIWORD
 
def get_version_number(filename):
    try:
        info = GetFileVersionInfo (filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    except:
        return "Unknown version"
 
if __name__ == "__main__":
  version = ".".join([str (i) for i in get_version_number (r'C:\Program Files\Internet Explorer\iexplore.exe')])
  print (version)
  
