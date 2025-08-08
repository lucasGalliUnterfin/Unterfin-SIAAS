import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
from datetime import datetime, timezone

# Para enviar notificaciones
from src.communication.mail import send_mail
from src.communication.slack import send_alert, send_alert_block

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

# Para clasificar noticias
#from src.classifiers.zero_shot import zero_shot_classify as classify_news


# Keywords para clasificar la severidad de las alertas
SEVERITY_KEYWORDS = {
    "rojo": ["bankruptcy", "default", "fraud", "collapse", "litigation", "sanction"],
    "amarillo": ["restructuring", "merger", "acquisition", "lawsuit", "fined", "downgrade"],
    "verde": ["deal", "agreement", "partnership", "negotiation", "settlement", "announcement"]
}

SEVERITY_MAPPING = {
    "rojo": 1,
    "amarillo": 2,
    "verde": 3
}

# Mapa de severidades para texto
SEVERITY_MAP = {
    1: "Alerta Roja",
    2: "Alerta Amarilla",
    3: "Alerta Verde"
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

## Aca quisiera cambiar esta funcion por alguna de los archivos de src/classifiers


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
# Formateo de alertas
####################################
def format_alerts_as_html(alerts_df):
    rows = []
    for _, row in alerts_df.iterrows():
        severity = int(row['severity'])
        severity_text = SEVERITY_MAP.get(severity, "Severidad sin clasificar")
        title = row["title"]
        desc = row["description"]
        url = row["url"]
        color = {1: "#e74c3c", 2: "#f39c12", 3: "#27ae60"}.get(severity, "#7f8c8d")

        html_row = f"""
        <tr>
            <td style="padding: 10px; border: 1px solid #ccc;">
                <strong>{title}</strong><br>
                <span style="color: {color}; font-weight: bold;">{severity_text}</span><br>
                {desc}<br>
                <a href="{url}">Leer más</a>
            </td>
        </tr>
        """
        rows.append(html_row)

    table = f"""
    <html>
    <body>
        <h2>🚨 Alertas Detectadas</h2>
        <table style="width:100%; border-collapse: collapse;">
            {''.join(rows)}
        </table>
    </body>
    </html>
    """
    return table


####################################
# Envio de notificaciones
####################################
def send_notifications(alerts_df):
    if alerts_df.empty:
        return

    html_body = format_alerts_as_html(alerts_df)
    send_mail("🚨 Nuevas alertas", html_body)

    for _, row in alerts_df.iterrows():
        sev = str(row["severity"])
        send_alert_block(row["title"], row["description"], row["url"], severity=sev)


####################################
# Proceso principal de alertas
####################################
def process_news():
    raw_news = get_news()

    alert_rows = []
    for item in raw_news:
        is_relevant, severity = classify_news(item)
        if is_relevant and severity is not None:
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