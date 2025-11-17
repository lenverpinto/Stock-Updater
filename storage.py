import json
import os
from detectors import md5_hash, normalize_html   # correct import

STATUS_FILE = "status.json"


def load_status():
    """Load saved state from status.json, or return empty dict if missing/corrupted."""
    if not os.path.exists(STATUS_FILE):
        return {}

    try:
        with open(STATUS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}  # fallback if the file is corrupted


def save_status(data):
    """Write updated state to status.json safely."""
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=4)


def extract_state(html, text, screenshot):
    """Return hash summary of page content for change detection."""
    return {
        "html_hash": md5_hash(normalize_html(html)),
        "text_hash": md5_hash(text),
        "img_hash": md5_hash(screenshot),
    }
