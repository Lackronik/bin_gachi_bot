import json

def initial_config(key):
    try:
        with open("api.json", "r") as read_file:
            config = json.load(read_file)
            return config.get(key)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {file_path}")
        print(e)
        return None