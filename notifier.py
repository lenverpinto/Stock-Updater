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

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


# ---------------- EMAIL ----------------
def send_email(message):
    try:
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
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot or chat ID not set. Skipping Telegram text alert.")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print("Telegram alert sent!", r.status_code)
    except Exception as e:
        print("Telegram send error:", e)


def send_telegram_photo(screenshot_path=None, screenshot_bytes=None, caption="Stock update!"):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot or chat ID not set. Skipping Telegram photo alert.")
        return
    try:
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
    if not WEBHOOK_URL:
        print("Webhook URL not set. Skipping webhook notification.")
        return
    try:
        requests.post(WEBHOOK_URL, json={"text": message})
        print("Webhook notification sent!")
    except Exception as e:
        print("Webhook send error:", e)


# ---------------- MAIN NOTIFY ----------------
def notify(message, screenshot_path=None, screenshot_bytes=None):
    if NOTIFY_EMAIL:
        send_email(message)

    if NOTIFY_TELEGRAM:
        if screenshot_path or screenshot_bytes:
            send_telegram_photo(screenshot_path=screenshot_path, screenshot_bytes=screenshot_bytes, caption=message)
        else:
            send_telegram_text(message)

    if NOTIFY_WEBHOOK:
        send_webhook(message)
