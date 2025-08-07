import feedparser
from datetime import datetime, timezone

def get_news() -> list[dict]:
    rss_url = "https://www.investing.com/rss/news_25.rss"  # Financial news
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries:
        news_items.append({
            "source": "Investing.com",
            "date": entry.get("published", datetime.now(timezone.utc).isoformat()),
            "title": entry.get("title", ""),
            "description": entry.get("summary", ""),
            "url": entry.get("link", "")
        })

    return news_items