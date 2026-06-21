# config_loader.py - Reads the maze configuration file

class Config:
    def __init__(self, filename: str):
        self.WIDTH = 0
        self.HEIGHT = 0
        self.ENTRY = (0, 0)
        self.EXIT = (0, 0)
        self.OUTPUT_FILE = ""
        self.PERFECT = False
        self._load(filename)

    def _load(self, filename: str):
        with open (filename , "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key == "WIDTH":
                    self.WIDTH = int(value)
                elif key == "HEIGHT":
                    self.HEIGHT = int(value)
                elif key == "ENTRY":
                    x, y = value.split(",")
                    self.ENTRY = (int(x), int(y))
                elif key == "EXIT":
                    x, y = value.split(",")
                    self.EXIT = (int(x), int(y))
                elif key == "OUTPUT_FILE":
                     self.OUTPUT_FILE = value
                elif key == "PERFECT":
                    self.PERFECT = value.lower() == "true"