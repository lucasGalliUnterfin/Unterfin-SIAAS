import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Cargar variables de entorno
def configure_env():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'claves.env'))

# Crear el engine de PostgreSQL
def get_db_engine():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(conn_str)

# Funciones de ingestión
def get_treasury_spread_fred():
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
    df["spread_2s10s"] = df["10Y"] - df["2Y"]
    df.index = pd.to_datetime(df.index)
    return df


def get_move_index(period="1y", interval="1d"):
    move = yf.download("^MOVE", period=period, interval=interval)

    # Si viene con multi-index, aplanar
    if isinstance(move.columns, pd.MultiIndex):
        move.columns = ['_'.join(col).strip() for col in move.columns.values]

    # Renombrar a una sola columna clara
    if "Close_^MOVE" in move.columns:
        move = move[["Close_^MOVE"]].rename(columns={"Close_^MOVE": "move_index"})
    else:
        move = move[["Close"]].rename(columns={"Close": "move_index"})

    move.index = pd.to_datetime(move.index)
    return move

# Guardar DataFrame en PostgreSQL
def save_to_postgres(df: pd.DataFrame, table_name: str):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists="append", index=True, index_label="date")
    print(f"Datos guardados en la tabla '{table_name}'")

# Punto de entrada
if __name__ == "__main__":
    configure_env()

    # Recuperar y guardar datos
    spread = get_treasury_spread_fred()
    save_to_postgres(spread, "treasury_spread")

    move = get_move_index()
    save_to_postgres(move, "move_index")
