import requests
import time
import json

class NewsBot:
    def __init__(self, config_path='config.json'):
        self.load_config(config_path)
        self.session = requests.Session()

    def load_config(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.channels = self.config.get("channels", [])
        self.start_message = self.config.get("start_message", "Hello! Here are your news updates:")
        self.format_str = self.config.get("format", "[{title}]({url})\n{summary}\n")
        self.interval = self.config.get("interval_minutes", 0)
        self.anime_feeds = self.config.get("anime_feeds", [])
        self.movies_feeds = self.config.get("movies_feeds", [])
        self.last_sent = {}

    def fetch_feed(self, url):
        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                import feedparser
                feed = feedparser.parse(resp.text)
                return feed.entries
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return []

    def get_new_articles(self, feed_url, feed_type):
        new_articles = []
        entries = self.fetch_feed(feed_url)
        last_sent_time = self.last_sent.get(feed_url, 0)
        for entry in entries:
            # Use published_parsed if available, otherwise skip
            published = entry.get("published_parsed")
            if not published:
                continue
            timestamp = time.mktime(published)
            if timestamp > last_sent_time:
                new_articles.append(entry)
                self.last_sent[feed_url] = max(self.last_sent.get(feed_url, 0), timestamp)
        return new_articles

    def format_article(self, entry):
        return self.format_str.format(
            title=entry.get("title", "No Title"),
            url=entry.get("link", "#"),
            summary=entry.get("summary", "")
        )

    def send_to_channel(self, channel, message):
        # Dummy implementation: print to console
        # Replace this with your bot framework's send message method
        print(f"[Channel: {channel}] {message}")

    def send_news(self):
        for channel in self.channels:
            msgs = [self.start_message]
            # Anime news
            for feed_url in self.anime_feeds:
                news = self.get_new_articles(feed_url, "anime")
                for entry in news:
                    msgs.append(self.format_article(entry))
            # Movies news
            for feed_url in self.movies_feeds:
                news = self.get_new_articles(feed_url, "movies")
                for entry in news:
                    msgs.append(self.format_article(entry))
            if len(msgs) > 1:
                msg = "\n".join(msgs)
                self.send_to_channel(channel, msg)

    def run(self):
        while True:
            self.send_news()
            print(f"Sleeping for {self.interval} minutes...")
            time.sleep(self.interval * 60)

if __name__ == "__main__":
    # Example config file should be created as 'config.json' in same directory
    bot = NewsBot()
    bot.run()