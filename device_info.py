import json

def get_password():
    with open("device_info.json") as f:
        info = json.load(f)
    return info["password"]

def set_password(password):
    with open("device_info.json") as f:
        info = json.load(f)
        info["password"] = password
    with open("device_info.json", "w") as f:
        json.dump(info, f)

def get_lock_image():
    with open("device_info.json") as f:
        info = json.load(f)
    return info["lock_image"]

def set_lock_image(path):
    with open("device_info.json") as f:
        info = json.load(f)
        info["lock_image"] = path
    with open("device_info.json", "w") as f:
        json.dump(info, f)

def get_home_image():
    with open("device_info.json") as f:
        info = json.load(f)
    return info["home_image"]

def set_home_image(path):
    with open("device_info.json") as f:
        info = json.load(f)
        info["home_image"] = path
    with open("device_info.json", "w") as f:
        json.dump(info, f)