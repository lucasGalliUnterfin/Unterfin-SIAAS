import os
import openai
from dotenv import load_dotenv

load_dotenv("claves.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
Eres un clasificador de noticias FINANCIERAS. *Todas* las noticias que recibes
provienen de fuentes económicas (Reuters, Bloomberg, TradingEconomics, etc.).  
Tu tarea es distinguir:

1. **Roja**: noticia financiera CRÍTICA que requiere acción inmediata.  
2. **Amarilla**: noticia financiera RELEVANTE que requiere monitoreo intensivo.  
3. **Verde**: noticia financiera POSITIVA, representa oportunidad de compra.  
4. **Ninguna**: noticia financiera IRRELEVANTE para decisiones de inversión.

Solo devuelves exactamente una de las etiquetas:  
`Roja`, `Amarilla`, `Verde` o `Ninguna`.
"""

FEW_SHOT_EXAMPLES = [
    {
        "news": "Volatility index spikes 20% amid uncertain market conditions",
        "label": "Ninguna"
    },
    {
        "news": "Major European bank faces liquidity crisis, government steps in",
        "label": "Roja"
    },
    {
        "news": "U.S. consumer price index rises slightly above expectations",
        "label": "Amarilla"
    },
    {
        "news": "Tech giant reports quarterly revenue 25% above forecasts",
        "label": "Verde"
    }
]

def classify_with_gpt(text: str) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for ex in FEW_SHOT_EXAMPLES:
        messages.append({
            "role": "user",
            "content": f"Noticia: {ex['news']}\nEtiqueta: {ex['label']}"
        })
    messages.append({
        "role": "user",
        "content": f"Noticia: {text}\nEtiqueta:"
    })

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0,
        max_tokens=4
    )
    label = resp.choices[0].message.content.strip()
    return label if label in {"Roja","Amarilla","Verde","Ninguna"} else "Ninguna"

print(classify_with_gpt("US Treasury yields surge 50 bps in one day, triggering margin calls across hedge funds"))