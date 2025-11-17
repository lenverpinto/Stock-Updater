# config.py
# Central configuration for the universal monitor project.
# Safe to commit — all secrets must come from environment variables.

import os

def env_int(varname, default):
    """Safely parse environment variable as int, fallback to default if missing or empty"""
    val = os.environ.get(varname)
    if val is None or val.strip() == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default

# ---------------- MONITOR / SCHEDULER ----------------
# Minutes between checks when running monitor.py in loop mode.
CHECK_INTERVAL_MIN = env_int("CHECK_INTERVAL_MIN", 5)

# Enable test mode? (prevents notifications)
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

# ---------------- KEYWORDS ----------------
KEYWORDS = [
    "in stock", "out of stock",
    "unavailable", "available",
    "sold out", "coming soon",
    "add to cart", "notify me",
    "back in stock", "only", "left", "available to ship"
]

# ---------------- TELEGRAM ----------------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
NOTIFY_TELEGRAM = os.environ.get("NOTIFY_TELEGRAM", "true").lower() == "true"

# ---------------- EMAIL ----------------
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "false").lower() == "true"
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = env_int("SMTP_PORT", 587)

# ---------------- WEBHOOK (Discord, Slack, Custom) ----------------
NOTIFY_WEBHOOK = os.environ.get("NOTIFY_WEBHOOK", "false").lower() == "true"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# ---------------- PLAYWRIGHT / FETCHER ----------------
PLAYWRIGHT_HEADLESS = os.environ.get("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
PLAYWRIGHT_NAV_TIMEOUT_MS = env_int("PLAYWRIGHT_NAV_TIMEOUT_MS", 0)
BLOCKED_RESOURCE_TYPES = ["image", "media", "font"]
FETCH_RETRIES = env_int("FETCH_RETRIES", 1)
POST_LOAD_WAIT_MS = env_int("POST_LOAD_WAIT_MS", 1500)

# ---------------- LOGGING / DEBUG ----------------
VERBOSE = os.environ.get("VERBOSE", "true").lower() == "true"

# ---------------- STORAGE ----------------
STATUS_FILE = os.environ.get("STATUS_FILE", "status.json")

# ---------------- SAFETY / RATE LIMITING ----------------
PER_HOST_MIN_DELAY_SEC = env_int("PER_HOST_MIN_DELAY_SEC", 1)
