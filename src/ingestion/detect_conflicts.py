import os
import requests
import sqlite3
from transformers import pipeline
from datetime import datetime
from dotenv import load_dotenv

# ! DISCLAIMER Esto es solo un overview de como seria la idea, hay problemas implementativos por todos lados a resolver


# ------------------------
# Configuración
# ------------------------
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = ["conflict", "trade agreement", "neutral"]

# ------------------------
# 1. Obtener noticias
# ------------------------
def fetch_news(query="trade OR conflict", language="en", page_size=10):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    if "articles" not in data:
        raise ValueError(f"Error en NewsAPI: {data}")
    return data["articles"]

# ------------------------
# 2. Clasificar con NLP
# ------------------------
def classify_text(text):
    result = classifier(text, candidate_labels=labels)
    return result["labels"][0], result["scores"][0]

# ------------------------
# 3. Guardar en SQLite
# ------------------------
def init_db():
    conn = sqlite3.connect("alerts.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            description TEXT,
            label TEXT,
            score REAL,
            published_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_alerts(articles):
    rows = []
    for art in articles:
        text = f"{art['title']} {art.get('description','')}"
        label, score = classify_text(text)
        rows.append((
            art["source"]["name"],
            art["title"],
            art.get("description",""),
            label,
            score,
            art.get("publishedAt", datetime.utcnow().isoformat())
        ))

    conn = sqlite3.connect("alerts.db")
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO alerts (source, title, description, label, score, published_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    conn.close()
    return rows

# ------------------------
# 4. Pipeline completo
# ------------------------
def run_pipeline():
    init_db()
    articles = fetch_news()
    results = save_alerts(articles)
    for r in results:
        print(f"📌 {r[1]} → {r[3]} ({r[4]:.2f})")

if __name__ == "__main__":
    run_pipeline()
