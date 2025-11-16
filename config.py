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
TEST_MODE=False
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
NOTIFY_TELEGRAM = True               # Enable/disable Telegram notifications
TELEGRAM_BOT_TOKEN = "8541693339:AAGXmigJDLG1R0vO9SEb6kOlMJqX1rhSttg"            # e.g. "123456:ABC-DEF..."
TELEGRAM_CHAT_ID =1111250499             # e.g. "123456789"

# curl.exe -F "chat_id=1111250499 " -F "caption=Test" -F "photo=@latest_snapshot.png" https://api.telegram.org/bot8541693339:AAGXmigJDLG1R0vO9SEb6kOlMJqX1rhSttg/sendPhoto


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
