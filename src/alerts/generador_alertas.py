import pandas as pd

# Definimos palabras clave que indican severidad
SEVERITY_LEVELS = {
    "high": ["lawsuit", "litigation", "bankruptcy", "fraud", "default", "prosecution", "criminal charges"],
    "medium": ["settlement", "fine", "penalty", "acquisition", "merger", "restructuring", "debt relief"],
    "low": ["agreement", "partnership", "deal", "joint venture", "cooperation"]
}

def classify_alert(text):
    """
    Clasifica si una noticia merece alerta y asigna severidad (low/medium/high).
    """
    text = str(text).lower()
    
    for level, keywords in SEVERITY_LEVELS.items():
        if any(k in text for k in keywords):
            return True, level  # merece alerta y severidad
    return False, None  # no merece alerta

def analyze_news(input_csv="../data/filtered_news.csv", output_csv="../data/analyzed_news.csv"):
    df = pd.read_csv(input_csv)

    alerts = []
    severities = []

    for _, row in df.iterrows():
        text = f"{row.get('title', '')} {row.get('description', '')}"
        is_alert, severity = classify_alert(text)
        alerts.append(is_alert)
        severities.append(severity)

    df["is_alert"] = alerts
    df["severity"] = severities

    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"✅ Análisis completado. Resultados guardados en {output_csv}")

analyze_news()
