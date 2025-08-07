import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv("claves.env")
API_KEY = os.getenv("FINNHUB_KEY")

def get_news() -> list[dict]:
    url = f"https://finnhub.io/api/v1/news?category=general&token={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    news_items = []

    for item in data:
        news_items.append({
            "source": "Finnhub",
            "date": datetime.fromtimestamp(item["datetime"], tz=timezone.utc).isoformat(),
            "title": item.get("headline", ""),
            "description": item.get("summary", ""),
            "url": item.get("url", "")
        })

    return news_items
