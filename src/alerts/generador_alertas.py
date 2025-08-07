import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from datetime import datetime, timezone

# Para enviar notificaciones
from src.communication.mail import send_mail
from src.communication.slack import send_alert

# Para obtener noticias de diferentes fuentes
from src.sources.finnhub import get_news as get_finnhub_news
from src.sources.google_news import get_news as get_google_news
from src.sources.investing import get_news as get_investing_news
from src.sources.reuters import get_news as get_reuters_news
from src.sources.trading_economics import get_news as get_trading_economics_news
# ! from src.sources.twitter_deltaone import get_news as get_twitter_deltaone_news
from src.sources.yahoo_finance import get_news as get_yahoo_finance_news

# Para insertar alertas en la base de datos
from src.queries.insert_alerts import insert_alerts


# Keywords para clasificar la severidad de las alertas
SEVERITY_KEYWORDS = {
    "rojo": ["bankruptcy", "default", "fraud", "collapse", "litigation", "sanction"],
    "amarillo": ["restructuring", "merger", "acquisition", "lawsuit", "fined", "downgrade"],
    "verde": ["deal", "agreement", "partnership", "negotiation", "settlement", "announcement"]
}

# Mapeo de severidades a números
SEVERITY_MAPPING = {
    "rojo": 1,
    "amarillo": 2,
    "verde": 3
}

# Mapa de severidades para texto
SEVERITY_MAP = {
    1: "🔴 ROJO",
    2: "🟡 AMARILLO",
    3: "🟢 VERDE"
}

####################################
# Obtencion de noticias 
####################################
def get_news():
    return (
        get_finnhub_news() + 
        get_google_news() +
        get_investing_news() +
        get_reuters_news() +
        get_trading_economics_news() +
        # ! get_twitter_deltaone_news() +
        get_yahoo_finance_news()
    )

####################################
# Clasificacion de noticias
####################################
def classify_news(item) -> tuple[bool, int | None]:
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()
    for level, keywords in SEVERITY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return True, SEVERITY_MAPPING[level]
    return False, None

####################################
# Guardado de noticias
####################################
def save_all_news():
    news_items = get_news()
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

    alerts_df["severity"] = alerts_df["severity"].astype(int)

    body_lines = []
    for _, row in alerts_df.iterrows():
        sev_label = SEVERITY_MAP.get(row["severity"], "SIN CLASIFICAR")
        emoji = sev_label.split()[0]  
        text = (
            f"{emoji} [{sev_label.split()[1]}]\n"
            f"📌 {row['title']}\n"
            f"📝 {row['description']}\n"
            f"🔗 {row['url']}"
        )
        body_lines.append(text)

    full_body = "\n\n" + "\n\n".join(body_lines)

    # Enviar por mail
    send_mail("🚨 NUEVAS ALERTAS", full_body)

    # Enviar por Slack (una por una)
    for msg in body_lines:
        send_alert(msg)


####################################
# Proceso principal de alertas
####################################
def process_news():
    raw_news = get_news()

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

    # Elimino los duplicados por URL
    df = df.drop_duplicates(subset="url")

    df.to_csv("data/alertas.csv", index=False)
    print(f"✅ {len(df)} alertas guardadas en data/alertas.csv")

    # Guardar las alertas en la base de datos
    if not df.empty: insert_alerts(df)

    # Enviar las notificaciones
    send_notifications(df)

save_all_news()
process_news()