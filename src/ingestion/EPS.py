import os
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf

load_dotenv("claves.env")


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
        
    
    print(f"Market cap total (en millones): {market_cap_total}")

    #Calculamos el EPS promedio pesado

    eps_promedio = eps_promedio/market_cap_total

    return ESPyMC, eps_promedio