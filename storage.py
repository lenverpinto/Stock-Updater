import json
import os
from detectors import md5_hash, normalize_html

STATUS_FILE = "status.json"

def load_status():
    if not os.path.exists(STATUS_FILE):
        return {}
    return json.load(open(STATUS_FILE))

def save_status(data):
    json.dump(data, open(STATUS_FILE, "w"), indent=4)

def extract_state(html, text, screenshot):
    return {
        "html_hash": md5_hash(normalize_html(html)),
        "text_hash": md5_hash(text),
        "img_hash": md5_hash(screenshot)
    }
