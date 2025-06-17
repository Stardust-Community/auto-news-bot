import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")  # channel or group (use @username or numeric ID)

FEEDS = [
    "https://www.animenewsnetwork.com/all/rss.xml",
    "https://www.imdb.com/news/movie/rss"
]