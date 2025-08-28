import os
import json


class Config:
    def __init__(self, path="config.json"):
        self.config = {
            "language": "en",
            "info-length": {
                "summary": 3,
                "definition": 15
                
            }
            
        }
        self.path = path
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                self.config = json.load(file)

    def save(self):
        with open(self.path, "w") as file:
            json.dump(self.config, file, indent=4)

    def update(self, path, value):
        
        keys = path.split(".")
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save()

    def get(self, path):
        keys = path.split(".")
        config = self.config
        for key in keys:
            if key not in config:
                return None
            config = config[key]
        return config