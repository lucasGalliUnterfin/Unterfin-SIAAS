from transformers import pipeline
import torch

# Para reproducibilidadad
import random
random.seed(42)
torch.manual_seed(42)


def get_classifier():
    # Usamos un modelo zero-shot para clasificar la importancia de las noticias financieras
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0 if torch.cuda.is_available() else -1,
        multi_label=True  # para poder asignar puntuaciones a varias opciones
    )
    return classifier


def classify_importance(news_text):
    classifier = get_classifier()

    # Usamos una escala ordinal de importancia de 0 a 10
    labels = [str(i) for i in range(11)]
    hypothesis_template = (
        "This financial news has an importance level of {} out of 10, "
        "where 0 means irrelevant and 10 means a critical market-moving event."
    )

    result = classifier(
        news_text,
        candidate_labels=labels,
        hypothesis_template=hypothesis_template
    )

    # Tomamos el label con mayor score como "rating final"
    best_label = result['labels'][0]
    best_score = result['scores'][0]

    return {
        "text": news_text,
        "predicted_importance": int(best_label),
        "confidence": round(best_score, 4),
        "distribution": dict(zip(result['labels'], result['scores']))
    }


if __name__ == "__main__":
    print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")

    test_headlines = [
        # 🔴 Altamente relevantes
        "US GDP unexpectedly shrinks by 1.2% in Q3, triggering fears of recession.",
        "Federal Reserve raises interest rates by 100 bps in emergency move.",
        "Major hedge fund collapses after bond market turmoil.",
        "Oil prices surge 12% after attack on Saudi production facilities.",
        "US inflation hits 9.1%, highest in four decades.",

        # 🟡 Relevantes, pero no urgentes
        "ECB signals possible rate hikes later this year.",
        "China’s exports rise modestly, indicating slow recovery.",
        "Argentina signs $45 billion IMF agreement renewal.",
        "Goldman Sachs revises S&P 500 year-end target to 4200.",

        # 🟢 Oportunidades o mejoras positivas
        "Tesla reports record quarterly earnings, stock jumps 7% in pre-market.",
        "Microsoft announces $10 billion investment in AI startup OpenAI.",
        "Brazil’s inflation slows for the third straight month.",

        # ⚪️ Irrelevantes financieramente
        "Lionel Messi wins his eighth Ballon d’Or.",
        "Apple introduces new color option for iPhone.",
        "Hollywood actor announces retirement from movies.",
        "Local weather disrupts city marathon in Tokyo."
    ]

    for headline in test_headlines:
        result = classify_importance(headline)
        print(f"\n📰 {headline}")
        print(f"→ Importance: {result['predicted_importance']} (Confidence: {result['confidence']})")
