import time
from pywinauto import Application
import os

import utl_win as uw
from utl_win import sleep

import re
import os
from datetime import datetime, timedelta


##########################################################
# App Environment 

class AppEnv:
    app = None
    wtop = None
    rib_tab = None
    rib_grp = None
    st_bar = None

    #private
    coh_path = None
    coh_exe = None

    def reset(self):
        self.app = None
        self.wtop = None
        self.rib_tab = None
        self.rib_grp = None
        self.st_bar = None
        
        #private
        coh_path = None
        coh_exe = None

    def placeholder(self, app):
        self.reset()
        
        self.app = app
        self.wtop = app.top_window()

        VERIFY(self.app, 'Application handler non Valid')
        VERIFY(self.wtop, 'Windows Application handler non Valid')

        if(not re.match('Starting Coherence.*', self.wtop.window_text())):
            self.rib_tab = uw.get_child_chk(self.wtop, name='Ribbon Tabs', ctrl_type='Group', deep=4, verify=False)      # TODO verify condizionale a wtop
            self.st_bar = uw.get_child_chk(self.wtop, name='StatusBar', ctrl_type='StatusBar', deep=4, verify=False)
            self.rib_grp = uw.get_child_chk(self.wtop, automation_id='59398', ctrl_type='ToolBar', deep=4, verify=False)

            VERIFY(self.rib_tab, 'Ribbon Tab handler non Valid')
            VERIFY(self.st_bar, 'Ribbon Bar handler non Valid')
            VERIFY(self.st_bar, 'Ribbon Group handler non Valid')

        #print (self)

    def init(self, coh_path): 
        self.reset()
        self.coh_path = coh_path
        self.coh_exe = os.path.basename(coh_path)

    def launch_app(self, coh_path, unique=True):
        self.init(coh_path)
        exe_name = os.path.basename(self.coh_path)

        if unique:
            found = 0
            try:
                app = Application(backend="uia").connect(path=self.coh_exe)
                found = 1
            except:
                pass
            VERIFY(not found, 'Coherence Already Started')
        
        try:
            print('Starting new instance...')
            app = Application(backend="uia").start(self.coh_path)
            time.sleep(1)                                               # TODO attesa attiva
            wtop = app.top_window()
        except Exception as e:
            RAISE(f"Start Error: {str(e)}")
            
        #print(f'app {app}')
        #print(f'wtop {wtop}')
        self.placeholder(app)

    def hang_app(self, coh_path):
        self.init(coh_path)
        hang_ok = 0
        self.reset()
        exe_name = os.path.basename(self.coh_path)
        
        try:
            app = Application(backend="uia").connect(path=self.coh_exe)
            wtop = app.top_window()
            hang_ok = 1
        except Exception as e:
            RAISE(f"Hang Error: {str(e)}")

        #print(f'app {app}')
        #print(f'wtop {wtop}')
        self.placeholder(app)

    def select_ribbon(self, ribb):
        rib_sel = uw.get_child_chk(self.rib_tab, name=ribb, ctrl_type='TabItem')
        uw.win_click(rib_sel)
        toolbar = uw.get_child_chk(self.rib_grp, name=ribb, ctrl_type='ToolBar')
        print(f'toolbar {toolbar}')
        return toolbar

    def select_ribbon_butt(self, ribb, butt):
        toolbar = self.select_ribbon(ribb)
        print(f'toolbar {toolbar}')
        bt = uw.get_child_chk(toolbar, name=butt, ctrl_type='Button', deep=2)
        return bt

    def click_ribbon_butt(self, ribb, butt, wait_end=1): 
        bt = self.select_ribbon_butt(ribb, butt)
        uw.win_click(bt)
        sleep(wait_end)
        return bt

    def ready(self):
        return self.app != None and self.wtop != None and self.rib_tab != None and self.rib_grp != None and self.st_bar != None

    def reload(self, wait_init=1, wait_in=1, wait_end=1, timeout=5):        
        now = datetime.now() 
        sleep(wait_init)
        run = 1
        while (run):
            try:
                app = Application(backend="uia").connect(path=self.coh_exe)
                wtop = app.top_window()
                status = 1
            except Exception as e:
                pass
            if app and wtop and not re.match('Starting Coherence.*', wtop.window_text()):
                status=2
                sleep(0.5)
                break
            elaps = (datetime.now()-now).seconds
            if (elaps>timeout):
                break
            sleep(wait_in)
        if status==2:
            sleep(wait_end)
            self.hang_app(self.coh_path)
        VERIFY(self.ready(), "Connection Was not Ready by Timeout")

env = AppEnv()              # session singleton

##########################################################
# App Options

class AppOptions:
    opt = None
    def set(self, options):
        self.opt = options
    def get(self, key):
        try:
            find_val = self.opt[key]
            return find_val
        except Exception as e:
            return None
         
opt = AppOptions()


##########################################################
# App Verifier - TODO Modulo Separato

import inspect
from PIL import ImageGrab, ImageDraw
import mouse
import shutil
import traceback

class Verifier:
    def __init__(self, log_file="dumps/error_log.txt", dump_dir="dumps"):
        self.log_file = log_file
        self.dump_dir = dump_dir
        #self.reset_dumps()
        os.makedirs(self.dump_dir, exist_ok=True)

    def reset_dumps(self):
        if os.path.exists(self.dump_dir):
            shutil.rmtree(self.dump_dir)
        os.makedirs(self.dump_dir)

    def _draw_cursor(self, image):
        cursor_x, cursor_y = mouse.get_position()
        screen_width, _ = ImageGrab.grab().size
        circle_radius = (screen_width / 100) * 2
        draw = ImageDraw.Draw(image)
        draw.ellipse(
            [
                (cursor_x - circle_radius, cursor_y - circle_radius),
                (cursor_x + circle_radius, cursor_y + circle_radius),
            ],
            outline="red",
            width=2,
        )
        return image

    def verify(self, condition, errormessage):
        if not condition:
            frame = inspect.currentframe().f_back.f_back
            lineno, filename = frame.f_lineno, frame.f_code.co_filename
            code_context = inspect.getframeinfo(frame).code_context[0].strip()
            function_name = frame.f_code.co_name

            filtered_stack = []
            for line in traceback.format_stack():
                filtered_stack.append(line)
                if "VERIFY(" in line:
                    break

            maxlev = 6
            filtered_stack.reverse()
            size=len(filtered_stack)
            if (size>maxlev):
                filtered_stack = filtered_stack[0:maxlev-1]
                filtered_stack.append(f'  ... {size-maxlev} more levels')

            screenshot = self._draw_cursor(ImageGrab.grab())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{self.dump_dir}/screenshot_{timestamp}_line{lineno}.png"
            screenshot.save(screenshot_path)

            with open(self.log_file, "a") as log_file:
                log_file.write(f"=== Error on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                log_file.write(f"Error in function '{function_name}' at line {lineno} in file {filename}:\n")
                log_file.write(f"Code: {code_context}\nMessage: {errormessage}\n")
                log_file.write(f"Screenshot saved at: {screenshot_path}\n\nStack Trace:\n")
                log_file.writelines(filtered_stack)
                log_file.write("\n")

            raise AssertionError(f"{errormessage}\nSee {self.log_file} and {screenshot_path} for details.")

verifier = Verifier()

def VERIFY(condition, errormessage):
    verifier.verify(condition, errormessage)

def RAISE(message):
    verifier.verify(False, message)


##########################################################
# Debug

if __name__ == '__main__':
    VERIFY(x == 11, "x should be 11")
