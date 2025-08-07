import os 
import pandas as pd 
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv("claves.env")



"""
 Corporate Net Cash Flow with IVA (CNCF):https://fred.stlouisfed.org/series/CNCF
 OBS: Las fechas deben estar en formato AAAA-MM-DD
"""
def get_cashFlow(fechaInicio,fechaFin):
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key)
    cp = fred.get_series(
    'BOGZ1FA895050005Q',
    observation_start= fechaInicio,  # fecha de inicializacion
    observation_end= fechaFin,    # fecha de finalizacion
    frequency='q'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = cp.reset_index()
    df.columns = ["Fecha","CNCF"]
    return df

