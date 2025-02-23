from pywinauto import Application
import os
import re
from datetime import datetime, timedelta
from PIL import ImageGrab, ImageDraw
import inspect
import mouse
import shutil
import traceback

class Verifier:
    def __init__(self, log_file="error_log.txt", dump_dir="dumps"):
        self.log_file = log_file
        self.dump_dir = dump_dir
        self.current_day_dir = None
        self.current_time_dir = None
        self._initialized = False  # Flag per verificare se l'istanza è stata inizializzata
        os.makedirs(self.dump_dir, exist_ok=True)

    def _ensure_initialized(self):
        """Inizializza l'istanza se non è già stata inizializzata."""
        if not self._initialized:
            self.init()

    def init(self):
        """Inizializza la struttura delle cartelle per il dump."""
        today = datetime.now().strftime("%Y%m%d")
        self.current_day_dir = os.path.join(self.dump_dir, f"DAY_{today}")
        os.makedirs(self.current_day_dir, exist_ok=True)
        self._initialized = True  # Imposta il flag di inizializzazione a True

    def clear(self, nday: int):
        """Cancella le cartelle più vecchie di nday giorni."""
        if not os.path.exists(self.dump_dir):
            return

        today = datetime.now()
        for folder_name in os.listdir(self.dump_dir):
            if folder_name.startswith("DAY_"):
                folder_date_str = folder_name.split("_")[1]
                folder_date = datetime.strptime(folder_date_str, "%Y%m%d")
                if (today - folder_date).days > nday:
                    folder_path = os.path.join(self.dump_dir, folder_name)
                    shutil.rmtree(folder_path)
                    print(f"Deleted old folder: {folder_path}")

    def reset_dumps(self):
        """Cancella tutti i dump precedenti."""
        if os.path.exists(self.dump_dir):
            shutil.rmtree(self.dump_dir)
        os.makedirs(self.dump_dir)

    def _draw_cursor(self, image):
        """Disegna il cursore sullo screenshot."""
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

    def dump(self, message, test_name=''):
        """Genera un report di errore."""
        self._ensure_initialized()  # Inizializza se necessario

        def make_stack_clickable(stacktrace: str) -> str:
            # Rende lo stack trace cliccabile
            lines = stacktrace.splitlines()
            result = []
            file_pattern = r'  File "(.*?)", line (\d+), in (.*?)$'
            for line in lines:
                match = re.match(file_pattern, line)
                if match:
                    filepath, line_num, function = match.groups()
                    clickable_line = f'  File [file:///{filepath}#L{line_num}], line {line_num}, in {function}'
                    result.append(clickable_line)
                else:
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
                parts = line.strip().split(", ")
                file_path = parts[0].replace("File \"", "").strip('"')
                line_number = parts[1].replace("line ", "").strip()
                func_name = parts[2].replace("in ", "").strip()
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

        # Crea il nome della cartella TIME
        timestamp = datetime.now().strftime("%H%M%S")
        time_folder_name = f"TIME_{timestamp}"
        if test_name:  # Se è specificato un test_name, aggiungilo al nome della cartella
            time_folder_name += f"_{test_name}"

        # Crea la cartella TIME per il dump corrente
        self.current_time_dir = os.path.join(self.current_day_dir, time_folder_name)
        os.makedirs(self.current_time_dir, exist_ok=True)

        # Cattura uno screenshot
        screenshot = self._draw_cursor(ImageGrab.grab())
        screenshot_path = os.path.join(self.current_time_dir, f"screenshot_line{lineno}.png")
        screenshot.save(screenshot_path)

        # Scrivi i dettagli dell'errore nel file di log
        log_path = os.path.join(self.current_time_dir, self.log_file)
        with open(log_path, "a") as log_file:
            log_file.write(f"====================================================================================\n")
            log_file.write(f"=== Error on test:{test_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            log_file.write(f"Error in function '{function_name}' at line {lineno} in file {filename}:\n")
            log_file.write(f"Code: {code_context}\nMessage: {message}\n")
            log_file.write(f"Screenshot saved at: {screenshot_path}\n\nStack Trace:\n")
            log_file.write(make_stack_clickable(stack_trace))
            log_file.write("\n")

        # Informa l'utente del percorso del dump
        print(f"== TEST FAIL =========================================================================================")
        print(f" * Error:      [{message}]")
        print(f" * File:       [{file_link} func:{function_name}]")
        print(f" * Dump to:    [{os.path.abspath(log_path)}]")
        print(f" * Screen to:  [{os.path.abspath(screenshot_path)}]")

# Funzione globale CLEAR
def CLEAR(nday: int):
    verifier.clear(nday)

# Inizializza il Verifier (senza invocazione diretta al momento dell'import)
verifier = Verifier()

def DUMP(message, test_name=''):
    verifier.dump(message, test_name)

def VERIFY(condition, message):
    if not condition:
        raise AssertionError(message)

def RAISE(message):
    VERIFY(False, message)