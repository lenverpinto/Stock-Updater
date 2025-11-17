# TELEGRAM_BOT_TOKEN = ""          # ← Add your bot token
# TELEGRAM_CHAT_ID = ""            # ← Add your chat ID

# CHECK_INTERVAL_MIN = 5           # Only used if you run monitor.py loop mode




# config.py
# -----------
# Central configuration for the universal monitor project.
# Replace the placeholder values with your own secrets where needed.

# ---------------- MONITOR / SCHEDULER ----------------
# Number of minutes to wait between checks when running in loop mode.
CHECK_INTERVAL_MIN = 5
# TEST_MODE=False
# If you prefer seconds or a one-off run you can override usage in monitor.py
# (monitor.py uses CHECK_INTERVAL_MIN in the examples earlier).

# ---------------- KEYWORDS ----------------
# Words that the detector will look for when deciding if a change is meaningful.
KEYWORDS = [
    "in stock", "out of stock",
    "unavailable", "available",
    "sold out", "coming soon",
    "add to cart", "notify me",
    "back in stock", "only", "left", "available to ship"
]

# ---------------- TELEGRAM (recommended) ----------------
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

NOTIFY_TELEGRAM = True               # Enable/disable Telegram notifications



# ---------------- EMAIL ----------------
NOTIFY_EMAIL = False                 # Enable/disable email notifications
EMAIL_FROM = ""                      # Sender address (Gmail recommended)
EMAIL_TO = ""                        # Recipient address
EMAIL_PASSWORD = ""                  # App password / SMTP password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ---------------- WEBHOOK (Discord/Slack/custom) ----------------
NOTIFY_WEBHOOK = False
WEBHOOK_URL = ""                     # Full webhook URL for POST requests

# ---------------- PLAYWRIGHT / FETCHER ----------------
# Toggle headless mode (set to False for debugging when you want to see the browser)
PLAYWRIGHT_HEADLESS = True

# If a site blocks headless Chrome, toggling headful may help.
# Set to 0 to disable the default navigation timeout (used in fetcher).
PLAYWRIGHT_NAV_TIMEOUT_MS = 0

# Optional: route-blocked resource types to speed up page loads (images/fonts/media)
# Keep as is unless you need images/screenshots to include images.
BLOCKED_RESOURCE_TYPES = ["image", "media", "font"]

# ---------------- RETRIES & TIMINGS ----------------
# How many times to retry fetching a page on failure (simple retry logic can use this)
FETCH_RETRIES = 1

# Milliseconds to wait after domcontentloaded before grabbing text/screenshot
POST_LOAD_WAIT_MS = 1500  # 1500ms = 1.5s

# ---------------- LOGGING / DEBUG ----------------
VERBOSE = True   # Set to False to reduce console logs

# ---------------- STORAGE ----------------
STATUS_FILE = "status.json"   # Path used by storage.py

# ---------------- SAFETY / RATE LIMITING ----------------
# Minimum seconds to sleep between requests to the same host (politeness)
PER_HOST_MIN_DELAY_SEC = 1

# ---------------- NOTES ----------------
# - Fill TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for instant Telegram alerts.
# - If you enable email, use an app password (Gmail) and set NOTIFY_EMAIL = True.
# - Keep secrets out of version control. Consider using environment variables for production.
