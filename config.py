import os

# Telegram Configuration
API_ID = int(os.getenv("API_ID", 22182189))
API_HASH = os.getenv("API_HASH", "5e7c4088f8e23d0ab61e29ae11960bf5")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", 6556141430))
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", -1001234567890))

# Database Configuration
DB_NAME = "tracker.db"
CHECK_INTERVAL = 300  # Default check interval in seconds
MAX_TRACKERS = 20

# URL Patterns
URL_REGEX = r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/\S*)?$'
