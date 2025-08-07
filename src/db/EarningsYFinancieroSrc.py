import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
from sqlalchemy import create_engine
from fredapi import Fred
import requests
from bs4 import BeautifulSoup
 
def configure_env():
    load_dotenv(os.path.join(os.path.__file___,'..','..','claves.env'))

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
Funcion que devuelve un dataframe con los n tickers mas alta con informacion de EPS y marketcap y un float que es
un EPS con promedios pesados segun marketcap total de los n tickers seleccionaods
( n<500 :) )
"""

def get_epsInd(n):

    avg_eps = 0
    eps_promedio = 0

    # Obenemos los tickers del S&P500 de wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sp500_table = pd.read_html(url)[0]
    tickers = sp500_table['Symbol'].tolist()
    tickers = tickers[:n]

    # Vamos a trabajar con las cifras en millones para evitar errores numéricos
    market_cap_total = 0

    # Dataframe con market cap y earnings per share del S&P500
    ESPyMC = pd.DataFrame(columns=['ticker', 'EPS', 'market cap'])

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            eps = info.get('trailingEps', None)
            market_cap = info.get('marketCap', None)

            if eps is not None and market_cap is not None:
                market_cap_milliones = market_cap / 1e6
                market_cap_total += market_cap_milliones
                eps_promedio += eps*market_cap_milliones

                fila_temp = pd.DataFrame([{
                    'ticker': ticker,
                    'EPS': eps,
                    'market cap': market_cap_milliones
                }])
                ESPyMC = pd.concat([ESPyMC, fila_temp], ignore_index=True)
        

        except Exception as e:
            print(f"Error con {ticker}: {e}")
        
    print(ESPyMC)
    print(f"Market cap total (en millones): {market_cap_total}")

    #Calculamos el EPS promedio pesado

    eps_promedio = eps_promedio/market_cap_total

    return ESPyMC, eps_promedio



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
#Funcional

"""
Corporate Profits After Tax (without IVA and CCAdj) (CP) :https://fred.stlouisfed.org/series/CP
OBS: el formator de la fecha debe ser "AAAA-MM-DD"
"""
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

"""
All Sectors; Total Capital Expenditures, Transactions (BOGZ1FA895050005Q): https://fred.stlouisfed.org/series/BOGZ1FA895050005Q
"Inversiones de capital totales"
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



"""
5.) Corporate Net Cash Flow with IVA (CNCF):https://fred.stlouisfed.org/series/CNCF
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
    df.columns = ["Fecha","Flujo de Fondos Corpo"]
    return df



#Main
if __name__ == "__main__":
    configure_env()


