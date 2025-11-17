import os
import requests
import smtplib
from email.mime.text import MIMEText
from PIL import Image
from io import BytesIO

# ---------------- CONFIG ----------------
NOTIFY_TELEGRAM = os.environ.get("NOTIFY_TELEGRAM", "true").lower() == "true"
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "false").lower() == "true"
NOTIFY_WEBHOOK = os.environ.get("NOTIFY_WEBHOOK", "false").lower() == "true"
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")


def env_int(varname, default):
    val = os.environ.get(varname)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default


SMTP_PORT = env_int("SMTP_PORT", 587)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


# ---------------- HELPER ----------------
def missing(*vars_list):
    return any(v is None or v == "" for v in vars_list)


# ---------------- EMAIL ----------------
def send_email(message):
    if missing(EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD):
        print("Email disabled: missing EMAIL_FROM / EMAIL_TO / EMAIL_PASSWORD")
        return
    try:
        if TEST_MODE:
            print("[TEST MODE] Email skipped:", message)
            return

        msg = MIMEText(message)
        msg["Subject"] = "Stock Alert"
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

        print("Email sent!")
    except Exception as e:
        print("Email send error:", e)


# ---------------- TELEGRAM ----------------
def send_telegram_text(message):
    if missing(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID):
        print("Telegram disabled: missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return
    try:
        if TEST_MODE:
            print("[TEST MODE] Telegram message skipped:", message)
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print("Telegram alert sent!", r.status_code)
    except Exception as e:
        print("Telegram send error:", e)


def send_telegram_photo(screenshot_path=None, screenshot_bytes=None, caption="Stock update!"):
    if missing(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID):
        print("Telegram disabled: missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return
    try:
        if TEST_MODE:
            print("[TEST MODE] Telegram photo skipped:", caption)
            return

        # Load image from path or bytes
        if screenshot_bytes:
            img = Image.open(BytesIO(screenshot_bytes))
        elif screenshot_path:
            img = Image.open(screenshot_path)
        else:
            print("No screenshot provided.")
            return

        # Resize to fit Telegram limits
        img.thumbnail((1280, 1280), Image.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        r = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
            files={"photo": ("screenshot.png", buffer)}
        )
        print("Telegram photo sent!", r.status_code)
    except Exception as e:
        print("Telegram photo send error:", e)


# ---------------- WEBHOOK ----------------
def send_webhook(message):
    if missing(WEBHOOK_URL):
        print("Webhook disabled: missing WEBHOOK_URL")
        return
    try:
        if TEST_MODE:
            print("[TEST MODE] Webhook skipped:", message)
            return

        requests.post(WEBHOOK_URL, json={"text": message})
        print("Webhook notification sent!")
    except Exception as e:
        print("Webhook send error:", e)


# ---------------- MAIN NOTIFY ----------------
def notify(message, screenshot_path=None, screenshot_bytes=None):
    print("Notify called with:", message)

    if NOTIFY_EMAIL:
        send_email(message)

    if NOTIFY_TELEGRAM:
        if screenshot_path or screenshot_bytes:
            send_telegram_photo(screenshot_path=screenshot_path, screenshot_bytes=screenshot_bytes, caption=message)
        else:
            send_telegram_text(message)

    if NOTIFY_WEBHOOK:
        send_webhook(message)
