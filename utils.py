import sys
import os
import json

USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "MyAppData", "YourApp")
os.makedirs(USER_DATA_DIR, exist_ok=True)

def user_file_path(filename):
    return os.path.join(USER_DATA_DIR, filename)

def ensure_json_file(filename, default_data):
    path = user_file_path(filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)
    return path

def ensure_txt_file(filename):
    path = user_file_path(filename)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
    return path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
