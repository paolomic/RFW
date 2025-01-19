######################################################
# RoboCop Interface
# Nota: per funzioni pyton non in locale importarle
# in un file locale  
# oppure usare:
#   $ robot --pythonpath . example.robot  


def test_dialog(argument):
    if (argument=='cappero'):
        return "ok"
    else:
        return "The provided string is not correct"
    