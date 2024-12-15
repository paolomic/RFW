
import winwatch as ww 
import util as util 

def window_handler(hwnd):
  print(ww.get_window_details(hwnd))

def main():
    print("=================================================")
    print("Sample Windows Tracker - Ctrl+C per interrompere.")
    tracker = ww.WindowTracker()

    hwin = util.get_main_wnd("Coherence - ", timeout_sec=10)
    if hwin:
       pid = hwin.process_id()
       if pid:
        tracker.start_tracking(window_handler, pid, "show", 60)

main()