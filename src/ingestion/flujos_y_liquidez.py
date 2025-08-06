import os
import requests
import pandas as pd
import yfinance as yf
import pandasdmx
from dotenv import load_dotenv

# Cargar variables desde claves.env
load_dotenv("claves.env")


def get_ted_spread_fred():
    """
    Descarga el TED Spread (3M Libor - 3M T-bill) desde FRED.
    """
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {"series_id": "TEDRATE", "api_key": api_key, "file_type": "json"}
    r = requests.get(url, params=params)
    resp = r.json()

    if "observations" not in resp:
        raise ValueError(f"Error fetching TEDRATE: {resp}")

    ted_spread = pd.Series(
        {obs["date"]: float(obs["value"]) for obs in resp["observations"] if obs["value"] != "."},
        name="TED_Spread"
    )

    df = ted_spread.to_frame()
    return df


def get_sofr_fred():
    """
    Descarga la serie SOFR desde FRED.
    Es posible que sea mejor descargarla de NY Fed porque parece tener informacion diaria que FRED no tiene
    """
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")

    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {"series_id": "SOFR", "api_key": api_key, "file_type": "json"}
    r = requests.get(url, params=params)
    resp = r.json()

    if "observations" not in resp:
        raise ValueError(f"Error fetching SOFR: {resp}")

    data = pd.Series(
        {obs["date"]: float(obs["value"]) for obs in resp["observations"] if obs["value"] != "."},
        name="SOFR"
    )
    df = data.to_frame()
    return df

get_ted_spread_fred()
get_sofr_fred()