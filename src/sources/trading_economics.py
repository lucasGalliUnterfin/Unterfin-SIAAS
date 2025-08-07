import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv("claves.env")
API_KEY = os.getenv("TE_KEY")

def get_news() -> list[dict]:
    url = f"https://api.tradingeconomics.com/news?c={API_KEY}&f=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    news_items = []

    for item in data:
        news_items.append({
            "source": "TradingEconomics",
            "date": item.get("date", datetime.now(timezone.utc).isoformat()),
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "url": item.get("url", "")
        })

    return news_items