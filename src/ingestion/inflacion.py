from dotenv import load_dotenv
import os
import pandas as pd
from fredapi import Fred

dotenv_path = os.path.join(os.path.dirname(__file__), "..", "..", "claves.env")
load_dotenv("claves.env")

"""
Inflación, usamos Fred para obtener una serie de tiempo de datos inflacionarios
URL de la seire de tiempo que estamos usando: https://fred.stlouisfed.org/series/CORESTICKM159SFRBATL

OBS: el formator de la fecha debe ser "AAAA-MM-DD"
"""
def get_inflacion(fechaInicio,fechaFin):
    
    api_key = os.getenv("FRED_API_KEY")
    
    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")

    fred = Fred(api_key)

    inflacionSerie = fred.get_series(
        'CORESTICKM159SFRBATL',
        observation_start= fechaInicio,  # fecha de inicializacion
        observation_end= fechaFin,    # fecha de finalizacion
        frequency='m'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = inflacionSerie.reset_index()
    df.columns = ["Fecha","Inflacion"]
    return df

