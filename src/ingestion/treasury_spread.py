import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Cargar variables desde claves.env
load_dotenv("claves.env")

# -------------------------
# US 2s10s Treasury Spread (FRED)
# -------------------------
def get_treasury_spread():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")

    series_ids = {"GS2": "2Y", "GS10": "10Y"}
    data = {}

    for fred_id, label in series_ids.items():
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {"series_id": fred_id, "api_key": api_key, "file_type": "json"}
        r = requests.get(url, params=params)
        resp = r.json()

        if "observations" not in resp:
            raise ValueError(f"Error fetching {fred_id}: {resp}")

        data[label] = pd.Series(
            {obs["date"]: float(obs["value"]) for obs in resp["observations"] if obs["value"] != "."}
        )

    df = pd.DataFrame(data)
    df["Spread_2s10s"] = df["10Y"] - df["2Y"]
    return df

get_treasury_spread()