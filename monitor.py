import time
from fetcher import fetch_page
from hashlib import md5
from notifier import notify
from config import CHECK_INTERVAL_MIN, TEST_MODE
import os
import json

STATUS_FILE = "status.json"

# ---------------- STORAGE ----------------
def load_status():
    if os.path.exists(STATUS_FILE):
        return json.load(open(STATUS_FILE))
    return {}

def save_status(status):
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f)

# ---------------- HASH ----------------
def md5_hash(data):
    if isinstance(data, bytes):
        return md5(data).hexdigest()
    if isinstance(data, str):
        return md5(data.encode("utf-8")).hexdigest()
    return md5(str(data).encode("utf-8")).hexdigest()

# ---------------- STOCK CHECK ----------------
def is_in_stock(text):
    """Check if product is in stock based on page text"""
    in_stock_keywords = ["In Stock", "Available", "Add to Cart", "Ships from"]
    text_lower = text.lower()
    for kw in in_stock_keywords:
        if kw.lower() in text_lower:
            return True
    return False

# ---------------- MONITOR ----------------
def monitor_once():
    urls = [line.strip() for line in open("urls.txt") if line.strip()]
    old_status = load_status()
    new_status = {}

    for url in urls:
        print(f"Checking: {url}")
        html, text, screenshot = fetch_page(url)

        text_hash = md5_hash(text)
        html_hash = md5_hash(html)
        img_hash = md5_hash(screenshot)
        currently_in_stock = is_in_stock(text)

        new_status[url] = {
            "html_hash": html_hash,
            "text_hash": text_hash,
            "img_hash": img_hash,
            "in_stock": currently_in_stock
        }

        # ---------------- ALERT LOGIC ----------------
        send_alert = False

        if TEST_MODE:
            send_alert = True  # always send in test mode
        else:
            if currently_in_stock:
                send_alert = True  # send alert only if product is in stock

        if send_alert:
            screenshot_path = "latest_snapshot.png"
            with open(screenshot_path, "wb") as f:
                f.write(screenshot)

            caption = f"🔔 Stock alert at: {url}"
            notify(caption, screenshot_path=screenshot_path)
            print("Alert sent.")
        else:
            print("No alert (item not in stock or no change).")

    save_status(new_status)

# ---------------- LOOP ----------------
def loop_mode():
    while True:
        monitor_once()
        print(f"Sleeping {CHECK_INTERVAL_MIN} minutes...\n")
        time.sleep(CHECK_INTERVAL_MIN * 60)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    loop_mode()
