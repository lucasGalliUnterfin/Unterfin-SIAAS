from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("claves.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # o directamente el string

def classify_with_gpt(text: str) -> dict:
    context = """You are a financial alert classifier. You must classify the following news headline into one of four categories:
    - Red: urgent and critical, immediate action needed.
    - Yellow: important, close monitoring needed.
    - Green: positive, market opportunity.
    - None: not relevant to financial markets, fundamentally not for decision making."""

    # Ejemplos de clasificación hechos con ChatGPT
    few_shot_examples = """
    Example 1:
    Headline: "European sovereign debt downgraded to junk by major rating agency amid default fears"
    Classification: Red

    Example 2:
    Headline: "Federal Reserve minutes hint at possible rate hike before year-end"
    Classification: Yellow

    Example 3:
    Headline: "NASDAQ closes at record high as tech giants beat earnings estimates"
    Classification: Green

    Example 4:
    Headline: "The Central Bank of Peru maintains interest rates unchanged at 6.75% for the third month in a row"
    Classification: None
    """

    system_prompt = context
    user_prompt = few_shot_examples + f"\nHeadline: \"{text}\"\nClassification:"

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
    )

    answer = completion.choices[0].message.content.strip()

    return answer

print(classify_with_gpt("US Treasury yields surge 50 bps in one day, triggering margin calls across hedge funds"))