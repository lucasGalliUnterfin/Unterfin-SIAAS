import os
import requests
import pandas as pd
from dotenv import load_dotenv

def get_tradingeconomics_news():
    """
    Descarga noticias desde TradingEconomics API.
    Retorna lista de diccionarios con noticias completas.
    """
    load_dotenv("claves.env")
    API_KEY = os.getenv("TE_KEY")

    if not API_KEY:
        raise ValueError("No se encontró la clave TE_KEY en claves.env")

    url = f"https://api.tradingeconomics.com/news?c={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise ConnectionError(f"Error {response.status_code}: {response.text}")

    return response.json()


# Cargar keywords desde archivo
def load_keywords(filepath="src/ingestion/keywords.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

# Filtrar noticias según keywords
def filter_news(news_list, keywords):
    filtered = [
        item for item in news_list
        if any(k in item.get("title", "").lower() or k in item.get("description", "").lower() for k in keywords)
    ]
    return filtered

def main():
    # Cargamos keywords
    keywords = load_keywords()

    news = get_tradingeconomics_news()

    filtered = filter_news(news, keywords)

    # Guardamos en DataFrame
    df = pd.DataFrame(filtered)[["date", "title", "description", "url"]]
    print(df.head())

    # 5. Guardamos en CSV
    df.to_csv("data/filtered_news.csv", index=False, encoding="utf-8")
    print(f"✅ Se guardaron {len(df)} noticias filtradas en data/filtered_news.csv")

main()