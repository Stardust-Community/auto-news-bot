import logging
import feedparser
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID, FEEDS
import time

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)

posted_links = set()

def fetch_and_post_news():
    global posted_links
    messages = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            if entry.link not in posted_links:
                title = entry.title
                link = entry.link
                summary = entry.summary if hasattr(entry, "summary") else ""
                msg = f"<b>{title}</b>\n{summary}\n<a href='{link}'>Read more</a>"
                messages.append(msg)
                posted_links.add(entry.link)
    for msg in messages:
        try:
            bot.send_message(
                chat_id=CHAT_ID,
                text=msg,
                parse_mode="HTML",
                disable_web_page_preview=False
            )
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_post_news, "interval", hours=1)
    scheduler.start()
    logging.info("News bot started! Press Ctrl+C to stop.")
    try:
        fetch_and_post_news()
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()