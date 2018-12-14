import json

def get_password():
    with open("device_info.json") as f:
        info = json.load(f)
    return info["password"]