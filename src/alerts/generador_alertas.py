import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

from src.communication.mail import send_mail
from src.communication.slack import send_alert

load_dotenv("claves.env")

API_KEY = os.getenv("TE_KEY")

SEVERITY_KEYWORDS = {
    "rojo": ["bankruptcy", "default", "fraud", "collapse", "litigation", "sanction"],
    "amarillo": ["restructuring", "merger", "acquisition", "lawsuit", "fined", "downgrade"],
    "verde": ["deal", "agreement", "partnership", "negotiation", "settlement", "announcement"]
}

####################################
# Obtencion de datos de TradingEconomics
####################################
def fetch_te_news():
    url = f"https://api.tradingeconomics.com/news?c={API_KEY}&f=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return response.json()

####################################
# Clasificacion de noticias
####################################
def classify_news(item):
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()
    for level, keywords in SEVERITY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return True, level
    return False, None

####################################
# Guardado de noticias
####################################
def save_all_te_news():
    news_items = fetch_te_news()
    rows = []

    for item in news_items:
        rows.append({
            "date": item.get("date", datetime.now(timezone.utc).isoformat()),
            "title": item.get("title"),
            "description": item.get("description"),
            "url": item.get("url"),
        })

    df = pd.DataFrame(rows)
    df.to_csv("data/news.csv", index=False)
    print(f"💾 {len(df)} noticias guardadas en data/news.csv")

####################################
# Envio de notificaciones
####################################
def send_notifications(alerts_df: pd.DataFrame):
    if alerts_df.empty:
        return

    body_lines = []
    for _, row in alerts_df.iterrows():
        line = f"[{row['severity'].upper()}] {row['title']}\n{row['description']}\n{row['url']}\n"
        body_lines.append(line)

    full_body = "\n\n".join(body_lines)

    # Enviar por mail
    send_mail("🚨 Alertas TradingEconomics", full_body)

    # Enviar por Slack
    for line in body_lines:
        send_alert(line.strip())

####################################
# Proceso principal de alertas
####################################
def process_te_news():
    raw_news = fetch_te_news()

    alert_rows = []
    for item in raw_news:
        is_alert, severity = classify_news(item)
        if is_alert:
            alert_rows.append({
                "date": item.get("date", datetime.now(timezone.utc).isoformat()),
                "title": item.get("title"),
                "description": item.get("description"),
                "url": item.get("url"),
                "severity": severity
            })

    df = pd.DataFrame(alert_rows)

    df.to_csv("data/alertas.csv", index=False)
    print(f"✅ {len(df)} alertas guardadas en data/alertas.csv")

    # Enviar las notificaciones
    send_notifications(df)

save_all_te_news()
process_te_news()