import os
from dotenv import load_dotenv
from fredapi import Fred
import pandas as pd

load_dotenv("claves.env")

"""
Business Expectations: Sales Revenue Growth (ATLSBUSRGEP) :https://fred.stlouisfed.org/series/ATLSBUSRGEP
OBS: el formator de la fecha debe ser "AAAA-MM-DD"
"""
def get_SRG(fechaInicio,fechaFin):
    api_key = os.getenv("FRED_API_KEY")
    fred = Fred(api_key)

    srg = fred.get_series(
    'ATLSBUSRGEP',
    observation_start= fechaInicio,  # fecha de inicializacion
    observation_end= fechaFin,    # fecha de finalizacion
    frequency='m'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = srg.reset_index()
    df.columns = ["Fecha","Creciemiento de Ganancias de Venta"]

    return df