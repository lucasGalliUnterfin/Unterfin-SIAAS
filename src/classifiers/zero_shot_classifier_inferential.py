from transformers import pipeline
import torch

# Define las hipótesis que se usarán para la inferencia textual
LABELS = {
    "Red": "This financial news requires immediate and urgent investor action.",
    "Yellow": "This financial news should be monitored as it may have medium-term impact.",
    "Green": "This financial news suggests a potential buying opportunity.",
    "None": "This financial news is irrelevant or has no significant market impact."
}

# Hipótesis explícita en formato inferencial
HYPOTHESIS_TEMPLATE = (
    "This financial news requires immediate and urgent investor action: {}. "
    "This financial news should be monitored as it may have medium-term impact: {}. "
    "This financial news suggests a potential buying opportunity: {}. "
    "This financial news is irrelevant or has no significant market impact: {}."
)


def get_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if torch.cuda.is_available() else -1)


classifier = get_classifier()

def classify_news(text):
    # Se generan las hipótesis para cada categoría
    hypotheses = list(LABELS.values())
    result = classifier(text, hypotheses, multi_label=True)

    scores = dict(zip(result['labels'], result['scores']))
    top_label = max(scores, key=scores.get)

    return {
        "label": top_label,
        "score": scores[top_label],
        "all_scores": scores
    }


# Ejemplos de prueba para validar comportamiento (con resultado esperado como comentario)
examples = [
    # Esperado: Red
    "US inflation rose to 4.2% in July, increasing pressure on the Federal Reserve.",
    # Esperado: None o Green (depende del sesgo hacia impacto tech)
    "Apple announces a new iPhone with better camera features.",
    # Esperado: Red
    "US GDP unexpectedly shrinks by 1.2% in Q3, triggering fears of recession.",
    # Esperado: Red
    "ECB cuts rates by 50 bps unexpectedly.",
    # Esperado: Yellow
    "Oil prices drop 7% after OPEC fails to reach deal.",
    # Esperado: None
    "Coca-Cola's quarterly earnings met expectations, no major surprises."
]

print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")

for t in examples:
    print(f"\n📰 {t}\n→ {classify_news(t)}")
