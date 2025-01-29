import json
import os

def load_json(filename, default_data=None):
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found. Creating a new one.")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=4)
    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: {filename} is corrupted. Resetting to default.")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=4)
        return default_data

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
