from pywinauto import Application
import os


import re
import os
from datetime import datetime, timedelta

from PIL import ImageGrab, ImageDraw

##########################################################
# App Verifier - TODO Modulo Separato

import inspect
import mouse
import shutil
import traceback
from datetime import datetime
import os

class Verifier:
    def __init__(self, log_file="dumps/error_log.txt", dump_dir="dumps"):
        self.log_file = log_file
        self.dump_dir = dump_dir
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

    def dump(self, message):
        def make_stack_clickable(stacktrace: str) -> str:
            # Split the stacktrace into lines
            lines = stacktrace.splitlines()
            result = []
            
            # Regex per identificare le righe con informazioni sul file
            file_pattern = r'  File "(.*?)", line (\d+), in (.*?)$'
            
            for line in lines:
                # Cerca match per le righe che contengono informazioni sul file
                match = re.match(file_pattern, line)
                if match:
                    filepath, line_num, function = match.groups()
                    # Crea il link cliccabile in formato semplificato
                    clickable_line = f'  File [file:///{filepath}#L{line_num}], line {line_num}, in {function}'
                    result.append(clickable_line)
                else:
                    # Mantieni le altre righe invariate
                    result.append(line)
            
            return '\n'.join(result)
        
        # Ottieni l'intera traccia dello stack
        stack_trace = traceback.format_exc()

        # Ottieni il frame corrente e il frame precedente
        frame = inspect.currentframe().f_back.f_back
        lineno, filename = frame.f_lineno, frame.f_code.co_filename
        code_context = inspect.getframeinfo(frame).code_context[0].strip()
        function_name = frame.f_code.co_name

        # Formatta il percorso del file come collegamento ipertestuale per VSCode
        file_link = f"{os.path.abspath(filename)}:{lineno}"

        # Filtra lo stack per includere solo le informazioni rilevanti
        filtered_stack = []
        for line in traceback.format_stack():
            if "File \"" in line and "line " in line:
                # Estrai il percorso del file, il numero di riga e il nome della funzione
                parts = line.strip().split(", ")
                file_path = parts[0].replace("File \"", "").strip('"')
                line_number = parts[1].replace("line ", "").strip()
                func_name = parts[2].replace("in ", "").strip()
                # Formatta come collegamento ipertestuale per VSCode
                formatted_line = f"saved to: {os.path.abspath(file_path)}:{line_number}  # {func_name}"
                filtered_stack.append(formatted_line)
            else:
                filtered_stack.append(line)
            if "VERIFY(" in line:
                break

        # Limita il numero di livelli dello stack
        maxlev = 7
        filtered_stack.reverse()
        size = len(filtered_stack)
        if size > maxlev:
            filtered_stack = filtered_stack[0:maxlev - 1]
            filtered_stack.append(f'  ... {size - maxlev} more levels')

        # Cattura uno screenshot
        screenshot = self._draw_cursor(ImageGrab.grab())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{self.dump_dir}/screenshot_{timestamp}_line{lineno}.png"
        screenshot.save(screenshot_path)

        # Scrivi i dettagli dell'errore nel file di log
        with open(self.log_file, "a") as log_file:
            log_file.write(f"====================================================================================\n")
            log_file.write(f"=== Error on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            log_file.write(f"Error in function '{function_name}' at line {lineno} in file {filename}:\n")
            log_file.write(f"Code: {code_context}\nMessage: {message}\n")
            log_file.write(f"Screenshot saved at: {screenshot_path}\n\nStack Trace:\n")
            #log_file.writelines(filtered_stack)
            log_file.write("\nFull Stack Trace:\n")
            log_file.write(make_stack_clickable(stack_trace))
            log_file.write("\n")

        # Informa l'utente del percorso del dump
        print(f"== TEST FAIL =========================================================================================")
        print(f" * Error:      [{message}]")
        print(f" * File:       [{file_link} func:{function_name}]")
        print(f" * Dump to:    [{os.path.abspath(self.log_file)}]")
        print(f" * Screen to:  [{os.path.abspath(screenshot_path)}]")

verifier = Verifier()

def DUMP(message):
    verifier.dump(message)

def VERIFY(condition, message):
    if not condition:
        raise AssertionError(message)

def RAISE(message):
    VERIFY(False, message)


