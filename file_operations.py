import json
import os

config_file = 'last_inputs.json'

def save_last_inputs(inputs):
    with open(config_file, 'w') as file:
        json.dump(inputs, file)

def load_last_inputs():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    return {}