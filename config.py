# config.py
# Central configuration for the universal monitor project.
# Safe to commit — all secrets must come from environment variables.

import os

# ---------------- MONITOR / SCHEDULER ----------------
# Minutes between checks when running monitor.py in loop mode.
CHECK_INTERVAL_MIN = int(os.environ.get("CHECK_INTERVAL_MIN", "5"))

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
# All must come from GitHub Actions → Settings → Secrets → Actions
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Toggle via environment, fallback = true
NOTIFY_TELEGRAM = os.environ.get("NOTIFY_TELEGRAM", "true").lower() == "true"


# ---------------- EMAIL ----------------
# Set NOTIFY_EMAIL=true in env to enable
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", "false").lower() == "true"

EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))


# ---------------- WEBHOOK (Discord, Slack, Custom) ----------------
NOTIFY_WEBHOOK = os.environ.get("NOTIFY_WEBHOOK", "false").lower() == "true"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")


# ---------------- PLAYWRIGHT / FETCHER ----------------
PLAYWRIGHT_HEADLESS = os.environ.get("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
PLAYWRIGHT_NAV_TIMEOUT_MS = int(os.environ.get("PLAYWRIGHT_NAV_TIMEOUT_MS", "0"))

BLOCKED_RESOURCE_TYPES = ["image", "media", "font"]

FETCH_RETRIES = int(os.environ.get("FETCH_RETRIES", "1"))
POST_LOAD_WAIT_MS = int(os.environ.get("POST_LOAD_WAIT_MS", "1500"))

# ---------------- LOGGING / DEBUG ----------------
VERBOSE = os.environ.get("VERBOSE", "true").lower() == "true"

# ---------------- STORAGE ----------------
STATUS_FILE = os.environ.get("STATUS_FILE", "status.json")

# ---------------- SAFETY / RATE LIMITING ----------------
PER_HOST_MIN_DELAY_SEC = int(os.environ.get("PER_HOST_MIN_DELAY_SEC", "1"))
