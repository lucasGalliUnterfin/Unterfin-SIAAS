from transformers import pipeline
from functools import lru_cache

# Etiquetas que usaremos en el modelo
CATEGORIES = [
    "Urgent market-moving alert",
    "Watchlist financial event",
    "Bullish opportunity",
    "Low-impact or irrelevant"
]


CONTEXT = """
You are a financial analyst assistant. Read the following news headline and classify it into one of these four categories:

1. Urgent financial event requiring immediate investor action (Red): Sudden, impactful events like interest rate surprises, geopolitical shocks, market crashes, or major institutional failures.
2. Market-relevant development that should be monitored closely (Yellow): Important financial signals like inflation changes, forward guidance, or macro trends.
3. Positive news suggesting a possible buying opportunity (Green): Signals of improved financial or economic conditions.
4. Irrelevant or minor financial news with no actionable value (None): Unimportant or off-topic news that should not trigger investor response.

Only choose one category that best reflects the headline’s relevance to active investors.
"""

@lru_cache()
def get_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli" # Se puede cambiar
    )

def classify_news(text: str) -> dict:
    classifier = get_classifier()

    full_text = f"{CONTEXT}\n\nNews: {text}"
    result = classifier(
        sequences=full_text,
        candidate_labels=CATEGORIES,
        multi_label=True
    )

    # Scores por clase
    scores = dict(zip(result["labels"], result["scores"]))

    # Elegir la categoría con mayor score si supera cierto umbral
    top_label, top_score = max(scores.items(), key=lambda x: x[1])
    threshold = 0.65  # Ajustable

    label = top_label if top_score > threshold else "Irrelevant or minor financial news with no actionable value (None)"

    return {
        "label": label,
        "score": top_score,
        "all_scores": scores
    }

# Para probarlo rápidamente

tests = [
    "US inflation rose to 4.2% in July, increasing pressure on the Federal Reserve.",
    "Apple announces a new iPhone with better camera features.",
    "US GDP unexpectedly shrinks by 1.2% in Q3, triggering fears of recession.",
    "ECB cuts rates by 50 bps unexpectedly.",
    "Oil prices drop 7% after OPEC fails to reach deal.",
    "Bolivia's Central Bank maintains interest rates unchanged at 6.75% for the third month in a row.",
    "The World Trade Center is destroyed in a terrorist attack.",
    "Congo's economy shows signs of recovery as mining output increases."
]

for t in tests:
    print(f"\n📰 {t}\n→ {classify_news(t)}")