import requests
from config import (
    NOTIFY_TELEGRAM,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    NOTIFY_EMAIL,
    EMAIL_FROM,
    EMAIL_TO,
    EMAIL_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    NOTIFY_WEBHOOK,
    WEBHOOK_URL
)
import smtplib
from email.mime.text import MIMEText
from PIL import Image

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

# ---------------- TELEGRAM TEXT ----------------
def send_telegram_text(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        })
        print("Telegram alert sent!", r.status_code)
    except Exception as e:
        print("Telegram send error:", e)

# ---------------- TELEGRAM PHOTO ----------------
def resize_image_for_telegram(image_path, max_width=1280, max_height=1280):
    img = Image.open(image_path)
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    resized_path = "resized_snapshot.png"
    img.save(resized_path)
    return resized_path

def send_telegram_photo(image_path, caption="Stock update!"):
    try:
        resized_path = resize_image_for_telegram(image_path)
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        with open(resized_path, "rb") as img_file:
            r = requests.post(
                url,
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
                files={"photo": img_file}
            )
        print("Telegram photo sent!", r.status_code)
    except Exception as e:
        print("Telegram photo send error:", e)

# ---------------- WEBHOOK ----------------
def send_webhook(message):
    try:
        requests.post(WEBHOOK_URL, json={"text": message})
        print("Webhook notification sent!")
    except Exception as e:
        print("Webhook send error:", e)

# ---------------- MAIN NOTIFY ----------------
def notify(message, screenshot_path=None):
    if NOTIFY_EMAIL:
        send_email(message)

    if NOTIFY_TELEGRAM:
        if screenshot_path:
            send_telegram_photo(screenshot_path, caption=message)
        else:
            send_telegram_text(message)

    if NOTIFY_WEBHOOK:
        send_webhook(message)
