from pywinauto.application  import Application
import time

## METODO 1

app = Application(backend="uia").connect(title="Untitled - Notepad")
notepad = app.window(title="Untitled - Notepad")                  # scorciatoia : app.UntitledNotepad

doc = notepad.child_window(control_type="Document")
doc.type_keys("Questo è un test di scrittura")


#app = Application("uia").start('notepad.exe')
app = Application(backend="uia").connect(title="Untitled - Notepad")
#notepad.Document.set_text("Questo è un test di scrittura")


#app = Application("uia").start('notepad.exe').connect(title = 'Untitled - Notepad', timeout = 2)        # win32
#app = Application("uia").connect(title = 'Untitled - Notepad', timeout = 2) 

#notepad = app.window(title="Untitled - Notepad")


#actionable_dlg = app.wait('visible')

#app.UntitledNotepad.print_control_identifiers()
#app.UntitledNotepad.type_keys("sticapperi e salciccie")

#app.UntitledNotepad.child_window(title="xx", control_type="Document")

# ---win32
#childwnd = app.UntitledNotepad.child_window(title="Untitled - Notepad", class_name="Notepad").wrapper_object()
#texteditor = childwnd.child_window(class_name="Windows.UI.Input.InputSite.WindowClass").wrapper_object()


#texteditor.type_keys("sticapperi e salciccie")

#time.sleep(2)
#app.kill()

