import inspect
from PIL import ImageGrab, ImageDraw
import os
from datetime import datetime
import mouse  # Usiamo il modulo mouse per ottenere la posizione del cursore
import shutil  # Per eliminare ricorsivamente la cartella dumps
import traceback  # Per ottenere l'intero stack di chiamate
import subprocess

path = r'D:\wsp_c'
path = os.path.realpath(path)

subprocess.run(["explorer", path])
exit()


os.startfile(path)                  # trova il tab se esiste gia
exit()
