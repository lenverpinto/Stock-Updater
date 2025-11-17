import json
import os
import time
from hashlib import md5

from fetcher import fetch_page
from detectors import diff_significant, md5_hash, normalize_html
from notifier import notify
from config import TEST_MODE, VERBOSE


STATUS_FILE = "status.json"


# ---------------- STORAGE ----------------
def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            return json.load(open(STATUS_FILE))
        except:
            return {}
    return {}


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)


def log(*args):
    if VERBOSE:
        print("[MONITOR]", *args)


# ---------------- MONITOR ONCE ----------------
def monitor_once():
    log("Starting monitor run...")

    urls = [line.strip() for line in open("urls.txt") if line.strip()]
    old_status = load_status()
    new_status = {}

    for url in urls:
        print(f"\nChecking: {url}")

        html, text, screenshot = fetch_page(url)

        # Normalize & hash
        clean_text = normalize_html(html)

        html_hash = md5_hash(html)
        text_hash = md5_hash(clean_text)
        img_hash = md5_hash(screenshot)

        old = old_status.get(url, {})

        was_html = old.get("html", "")
        was_text = old.get("text", "")
        was_img_hash = old.get("img_hash", "")

        # -------- Check for meaningful change --------
        changed = diff_significant(
            was_html,
            html,
            was_text,
            clean_text,
            was_img_hash,
            img_hash
        )

        # Save new status
        new_status[url] = {
            "html": html,
            "text": clean_text,
            "html_hash": html_hash,
            "text_hash": text_hash,
            "img_hash": img_hash
        }

        # -------- ALERT HANDLING --------
        if TEST_MODE:
            print("TEST_MODE = True → Forcing alert for testing.")

        if changed or TEST_MODE:
            screenshot_path = "latest_snapshot.png"
            with open(screenshot_path, "wb") as f:
                f.write(screenshot)

            caption = f"🔔 Change detected at:\n{url}"
            notify(caption, screenshot_path=screenshot_path)
            print("Alert sent!")
        else:
            print("No meaningful change.")

    save_status(new_status)
    log("Monitor run complete.")


# ---------------- MAIN (GitHub Actions uses single run) ----------------
if __name__ == "__main__":
    monitor_once()
