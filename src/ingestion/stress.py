import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv("claves.env")

"""
Stess tests: Usams la informacion disponible en fred, St. Louis Fed Financial Stress Index (STLFSI4)
URL de informacion: https://fred.stlouisfed.org/series/STLFSI4

OBS: el formator de la fecha debe ser "AAAA-MM-DD"
"""
def get_stress(fechaInicio,fechaFin):

    api_key = os.getenv('FRED_API_KEY')
    
    fred = Fred(api_key)
 
    stress = fred.get_series(
    'STLFSI4',
    observation_start= fechaInicio,  # fecha de inicializacion
    observation_end= fechaFin,    # fecha de finalizacion
    frequency='w'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )
    df = stress.reset_index()
    df.columns = ["Fecha","stress"]
    return df

