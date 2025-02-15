import json

class TestConfig:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TestConfig, cls).__new__(cls)
            cls._instance.config = {}
        return cls._instance

    def load(self, config_file: str):
        with open(config_file, "r") as file:
            self.config = json.load(file)
            print("Configurazione caricata:", self.config)

    def get(self, grp: str, key: str = None):
        if key is None:
            if '.' not in grp:
                raise ValueError("Formato non valido. Usa 'gruppo.chiave' o fornisci due argomenti separati.")
            grp, key = grp.split('.')
        try:
            return self.config[grp][key]
        except KeyError:
            raise KeyError(f"Chiave non trovata: gruppo '{grp}', chiave '{key}'")

config = TestConfig()           # singleton rimappa new

    