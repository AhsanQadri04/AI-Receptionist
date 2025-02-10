import json
import os

def load_json(filename, default_data=None):
    """Loads a JSON file. If missing or corrupted, resets it with default data."""
    if default_data is None:
        default_data = {}

    if not os.path.exists(filename):
        print(f"Warning: {filename} not found. Creating a new one with default data.")
        save_json(filename, default_data)
        return default_data

    try:
        with open(filename, encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(f"Warning: {filename} is corrupted. Resetting to default data.")
        save_json(filename, default_data)
        return default_data

def save_json(filename, data):
    """Saves data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
