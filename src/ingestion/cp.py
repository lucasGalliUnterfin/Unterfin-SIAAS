import os 
from dotenv import load_dotenv
import pandas as pd
from fredapi import Fred

load_dotenv("claves.env")

def get_CP(fechaInicio,fechaFin):
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key)
    cp = fred.get_series(
    'CP',
    observation_start= fechaInicio,  # fecha de inicializacion
    observation_end= fechaFin,    # fecha de finalizacion
    frequency='q'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = cp.reset_index()
    df.cp = ["Fecha","Sales Revenue Growth"]

    return df
