import inspect
from PIL import ImageGrab, ImageDraw
import os
from datetime import datetime
import mouse  # Usiamo il modulo mouse per ottenere la posizione del cursore
import shutil  # Per eliminare ricorsivamente la cartella dumps
import traceback  # Per ottenere l'intero stack di chiamate

class Verifier:
    def __init__(self, log_file="dumps/error_log.txt", dump_dir="dumps"):
        self.log_file = log_file
        self.dump_dir = dump_dir
        if not os.path.exists(self.dump_dir):
            os.makedirs(self.dump_dir)

    def reset_dumps(self):
        """Resetta tutto il contenuto della cartella dumps, inclusi log e immagini."""
        if os.path.exists(self.dump_dir):
            shutil.rmtree(self.dump_dir)  # Elimina ricorsivamente la cartella dumps
        os.makedirs(self.dump_dir)  # Ricrea la cartella dumps

    def _draw_cursor(self, image):
        """Disegna un cerchio rosso intorno alla posizione del cursore, 4 volte più grande."""
        draw = ImageDraw.Draw(image)
        
        # Ottieni la posizione del cursore usando il modulo mouse
        cursor_x, cursor_y = mouse.get_position()  # Ottieni la posizione del cursore

        # Calcola il diametro del cerchio come 4/100 della larghezza dello schermo
        screen_width, _ = ImageGrab.grab().size  # Ottieni la larghezza dello schermo dallo screenshot
        circle_diameter = (screen_width / 100) * 4  # Diametro del cerchio (4 volte più grande)
        circle_radius = circle_diameter / 2  # Raggio del cerchio

        # Disegna il cerchio rosso
        draw.ellipse(
            [
                (cursor_x - circle_radius, cursor_y - circle_radius),  # Angolo superiore sinistro
                (cursor_x + circle_radius, cursor_y + circle_radius),  # Angolo inferiore destro
            ],
            outline="red",  # Colore del bordo del cerchio
            width=2,  # Spessore del bordo
        )
        return image

    def verify(self, condition, errormessage):
        """Verifica una condizione e, se falsa, salva un dump con data, riga, funzione, screenshot, stack trace e messaggio di errore."""
        if not condition:
            # Ottieni il frame della funzione chiamante (due livelli sopra)
            frame = inspect.currentframe().f_back.f_back  # Risali di due frame
            lineno = frame.f_lineno  # Riga di codice
            filename = frame.f_code.co_filename  # Nome del file
            code_context = inspect.getframeinfo(frame).code_context[0].strip()  # Contesto del codice
            function_name = frame.f_code.co_name  # Nome della funzione

            # Ottieni l'intero stack di chiamate
            stack_trace = traceback.format_stack()  # Formatta l'intero stack di chiamate

            # Cattura lo screenshot
            screenshot = ImageGrab.grab()

            # Disegna il cerchio rosso intorno al cursore
            screenshot = self._draw_cursor(screenshot)

            # Salva lo screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"{self.dump_dir}/screenshot_{timestamp}_line{lineno}.png"
            screenshot.save(screenshot_path)

            # Scrivi il dump nel file di log
            with open(self.log_file, "a") as log_file:
                log_file.write(f"=== Error on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                log_file.write(f"Error in function '{function_name}' at line {lineno} in file {filename}:\n")
                log_file.write(f"Code: {code_context}\n")
                log_file.write(f"Message: {errormessage}\n")
                log_file.write(f"Screenshot saved at: {screenshot_path}\n")
                log_file.write("\nStack Trace:\n")
                log_file.writelines(stack_trace)  # Scrivi l'intero stack di chiamate
                log_file.write("\n")

            # Solleva l'eccezione con il messaggio di errore
            raise AssertionError(f"{errormessage}\nSee {self.log_file} and {screenshot_path} for details.")

# Istanza globale della classe Verifier
verifier = Verifier()

# Funzione VERIFY che può essere chiamata senza prefissi
def VERIFY(condition, errormessage):
    verifier.verify(condition, errormessage)

# Esempio di utilizzo
def test_function():
    x = 10
    VERIFY(x == 11, "x should be 11")  # <=== Questa è la riga che verrà registrata

def another_function():
    test_function()

# Resetta tutto il contenuto della cartella dumps all'inizio (opzionale)
verifier.reset_dumps()

try:
    another_function()
except AssertionError as e:
    print(e)