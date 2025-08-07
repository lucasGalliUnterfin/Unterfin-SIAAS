import os 
from dotenv import load_dotenv
import pandas as pd
from fredapi import Fred

load_dotenv("claves.env")
"""
All Sectors; Total Capital Expenditures, Transactions (BOGZ1FA895050005Q): https://fred.stlouisfed.org/series/BOGZ1FA895050005Q
"Inversiones de capital totales"
OBS: Las fechas debe estar en el formato AAAA-MM-DD
"""
def get_TotalExp(fechaInicio,fechaFin):
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key)
    cp = fred.get_series(
    'BOGZ1FA895050005Q',
    observation_start= fechaInicio,  # fecha de inicializacion
    observation_end= fechaFin,    # fecha de finalizacion
    frequency='q'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = cp.reset_index()
    df.columns = ["Fecha","Ganancia Corporativa"]
    return df

