######################################################
# RoboCop Interface
# Nota: per funzioni pyton non in locale importarle
# in un file locale  
# oppure usare:
#   $ robot --pythonpath . example.robot  


class TestResult:
    def __init__(self, status="ok", data=None, info=None):
        self.status = status
        self.data = data
        self.error_message = info
    def get(self): 
        return {
            "status": self.status,
            'data': self.data,
            'info': self.error_message}


def test_dialog(argument):
     return TestResult('ok', 'xx', 'yy').get()
     
     return xxx
    