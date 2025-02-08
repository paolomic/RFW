import win32gui
import win32con
import ctypes
from ctypes import wintypes
import time
import signal
import sys
import win32process

def signal_handler(sig, frame):
    print('Interrupt detected. Shutting down...')
    WindowTracker.ender = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class WindowTracker:
    ender = False
    callback = None
    user32 = ctypes.windll.user32

    def __init__(self):
        # Define callback prototype
        self.WinEventProc = ctypes.WINFUNCTYPE(
            None, 
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.HWND,
            wintypes.LONG,
            wintypes.LONG,
            wintypes.DWORD,
            wintypes.DWORD
        )
        self.ender = False
        self.callback = None

    def is_main_window(self, hwnd):
        """Check if window is a main application window"""
        if not self.user32.IsWindowVisible(hwnd):
            return False
            
        # Check if window has a parent (main windows don't)
        if self.user32.GetParent(hwnd):
            return False
            
        # Verify window has a title
        if self.user32.GetWindowTextLengthW(hwnd) == 0:
            return False
            
        # Check window styles
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        if not (style & win32con.WS_OVERLAPPEDWINDOW):
            return False
            
        return True

    def on_window_event(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        try:
            if not hwnd:
                return
                
            # Only process main windows
            if not self.is_main_window(hwnd):
                return

            # Get window text
            text = win32gui.GetWindowText(hwnd)
            if not text:
                return
            
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]

            # Call callback with window handle and text
            self.callback(pid, hwnd, text)

        except Exception as e:
            print(f"Error processing window event: {e}")

    def start_tracking(self, callback, event_type="both", timeout=0):
        """
        Start tracking window events
        event_type: "create", "show", or "both"
        """
        try:
            self.callback = callback
            
            # Create callback wrapper
            win_event_proc = self.WinEventProc(self.on_window_event)
            
            hooks = []
            
            # Set up hooks based on event type
            if event_type in ["create", "both"]:
                create_hook = self.user32.SetWinEventHook(
                    win32con.EVENT_OBJECT_CREATE,
                    win32con.EVENT_OBJECT_CREATE,
                    0,
                    win_event_proc,
                    0,
                    0,
                    win32con.WINEVENT_OUTOFCONTEXT
                )
                if create_hook:
                    hooks.append(create_hook)
                
            if event_type in ["show", "both"]:
                show_hook = self.user32.SetWinEventHook(
                    win32con.EVENT_OBJECT_SHOW,
                    win32con.EVENT_OBJECT_SHOW,
                    0,
                    win_event_proc,
                    0,
                    0,
                    win32con.WINEVENT_OUTOFCONTEXT
                )
                if show_hook:
                    hooks.append(show_hook)

            if not hooks:
                print("Failed to set window hooks")
                return

            # Message pump
            msg = ctypes.wintypes.MSG()
            start_time = time.time()
            
            while True:
                if timeout and time.time() > start_time + timeout:
                    print("Timeout reached")
                    break
                    
                if self.ender:
                    print("User break detected")
                    break

                while self.user32.PeekMessageA(ctypes.byref(msg), None, 0, 0, 0x0001):
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
                    
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Monitoring interrupted")
        except Exception as e:
            print(f"Tracking error: {e}")
        finally:
            # Remove all hooks
            for hook in hooks:
                self.user32.UnhookWinEvent(hook)

# Example usage
if __name__ == "__main__":
    def window_callback(hwnd, text):
        print(f"Window event detected - Handle: {hwnd}, Title: {text}")
        
    tracker = WindowTracker()
    tracker.start_tracking(window_callback, event_type="both", timeout=60)