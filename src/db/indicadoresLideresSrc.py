import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fredapi import Fred
import requests
from bs4 import BeautifulSoup



# Cargar variables de entorno
def configure_env():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'claves.env'))

# Crear el engine de PostgreSQL
def get_db_engine():
    user = os.getenv("SUPABASE_USER")
    password = os.getenv("SUPABASE_PASSWORD")
    host = os.getenv("SUPABASE_HOST")
    port = os.getenv("SUPABASE_PORT")
    db = os.getenv("SUPABASE_DB")

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?sslmode=require"

    return create_engine(conn_str)


# Guardar DataFrame en PostgreSQL
def save_to_postgres(df: pd.DataFrame, table_name: str):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists="replace", index=True, index_label="date")
    print(f"Datos guardados en la tabla '{table_name}'")

"""
Inflación, usamos Fred para obtener una serie de tiempo de datos inflacionarios
URL de la seire de tiempo que estamos usando: https://fred.stlouisfed.org/series/CORESTICKM159SFRBATL

OBS: el formator de la fecha debe ser "AAAA-MM-DD"
"""

def get_inflation(fechaInicio,fechaFin):
    
    api_key = os.getenv("FRED_API_KEY")
    
    if not api_key:
        raise ValueError("⚠️ FRED_API_KEY no configurada en claves.env")


    fred = Fred(api_key)


    inflacionSerie = fred.get_series(
        'CORESTICKM159SFRBATL',
        observation_start= fechaInicio,  # fecha de inicializacion
        observation_end= fechaFin,    # fecha de finalizacion
        frequency='a'                    # Tipos de frecuencia: 'm', 'q', 'sa', 'a'
    )

    df = inflacionSerie.reset_index()
    df.columns = ["Fecha","Flujo de Fondos Corpo"]
    return df


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



"""
PMI: Escrapeamos datos del ISM usando beautiful soup, tomamos los PMI de manufactura y de servicio.
Para ver el origen de los datos usar URL
"""
def get_PMI():

    # URL del informe ISM - Manufactura
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/pmi/july/"

    # Scrapeo de la tabla de manufactura
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')


    PMI_manufacture = pd.read_html(str(tables))[0]
    PMI_manufacture = PMI_manufacture.iloc[:-3]

    # URL del informe ISM - Serivicio
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/services/june/"

    # sScrapeo de la table de serivicios
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all tables
    tables = soup.find_all('table')

    PMI_service = pd.read_html(str(tables))[0]
    PMI_service = PMI_service.iloc[:-3]

    return PMI_manufacture,PMI_service

# Punto de entrada
if __name__ == "__main__":
    configure_env()


    