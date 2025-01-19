
import win32.lib.win32con as win32con


######################################################################################################
#region Robot Call 
######################################################################################################


#WM_ROBOT_GRID_COMMAND      = win32con.WM_USER + 199

ROBOT_MAX_BUFFER_SIZE       = 4096                              # ?
ROBOT_PORT                  = 63888                             # reply
ROBOT_SIGNATURE             = 55555                             # check sender
ROBOT_CMD_BASE              = 22220                             # aske fun
ROBOT_CMD_GET_HEADER        = ROBOT_CMD_BASE + 0
ROBOT_CMD_GET_PROP          = ROBOT_CMD_BASE + 1
ROBOT_CMD_IS_COL_VISIBLE    = ROBOT_CMD_BASE + 2
ROBOT_CMD_GET_COL_POINT     = ROBOT_CMD_BASE + 3

import win32gui
import socket
import ctypes

class RobotCommunicator:
    def __init__(self, window_handle):
        self.window_handle = window_handle
        self.server = None
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.server:
            self.server.close()
            
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', ROBOT_PORT))
        self.server.listen(1)
        return self.server
        
    def send_command(self, command_id, input_str, timeout):
        try:
            # Prepare data structure
            class COPYDATASTRUCT(ctypes.Structure):
                _fields_ = [
                    ("dwData", ctypes.wintypes.LPARAM),
                    ("cbData", ctypes.wintypes.DWORD),
                    ("lpData", ctypes.c_void_p)
                ]
            
            # Encode input data
            data = input_str.encode('utf-8') if input_str else b''
            buffer = ctypes.create_string_buffer(data)
            
            # Setup COPYDATA structure
            cds = COPYDATASTRUCT()
            cds.dwData = command_id
            cds.cbData = len(data)
            cds.lpData = ctypes.cast(buffer, ctypes.c_void_p).value
            
            wparam = (ROBOT_SIGNATURE << 16) | ROBOT_PORT
            
            # Start server before sending message
            self.start_server()
            self.server.settimeout(timeout)  # 2 seconds timeout
            
            # Send message
            result = win32gui.SendMessage(
                self.window_handle,
                win32con.WM_COPYDATA,
                wparam,
                ctypes.addressof(cds)
            )
            
            if result == 1:
                return self._receive_response()
            
            return result
            
        except Exception as e:
            print(f"Error in send_command: {e}")
            return None
            
    def _receive_response(self):
        try:
            client_socket, _ = self.server.accept()
            data = client_socket.recv(ROBOT_MAX_BUFFER_SIZE).decode('utf-8')
            client_socket.close()
            return data
        except socket.timeout:
            print("Socket timeout while waiting for response")
            return None
        except Exception as e:
            print(f"Error receiving response: {e}")
            return None

def robot_send(window_handle, command_id, input_str="", timeout = 2):
    with RobotCommunicator(window_handle) as communicator:
        return communicator.send_command(command_id, input_str, timeout=timeout)


#endregion
