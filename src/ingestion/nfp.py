import os
from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv

load_dotenv("claves.env")

"""
NFP: Non-farm Payroll
URL: https://fred.stlouisfed.org/series/ADPWNUSNERSA
Nombre de series de tiempo: Total Nonfarm Private Payroll Employment
"""
def get_NFP(fechaInicio,fechaFin):
    #Configuracion de API fred
    api_key = os.getenv("FRED_API_KEY")

    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")


    fred = Fred(api_key)
    #Relevamiento de datos
    NFPSerie = fred.get_series(
        'ADPWNUSNERSA',
        observation_start= fechaInicio,  # fecha de inicializacion
        observation_end= fechaFin,    # fecha de finalizacion
        frequency='w'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )
        

    df = NFPSerie.reset_index()
    df.columns = ["Fecha","Non-farm Payroll"]

    return df

