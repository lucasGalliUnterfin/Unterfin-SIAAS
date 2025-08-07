import feedparser
from datetime import datetime, timezone

def get_news() -> list[dict]:
    rss_url = "https://news.google.com/rss/search?q=finance+OR+merger+OR+acquisition&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    return [
        {
            "source": "Google News",
            "date": entry.get("published", datetime.now(timezone.utc).isoformat()),
            "title": entry.get("title", ""),
            "description": entry.get("summary", ""),
            "url": entry.get("link", "")
        }
        for entry in feed.entries[:10]
    ]

get_news()