import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import requests

load_dotenv("claves.env")
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
    PMI_manufacture["Series Index Jul"] = PMI_manufacture["Series Index Jul"].astype(float)
    PMI_manufacture["Series Index Jun"] = PMI_manufacture["Series Index Jul"].astype(float)

    # URL del informe ISM - Serivicio
    url = "https://www.ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business/services/july/"

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
    PMI_service = PMI_service.iloc[:,:-3]
    #PMI_service = PMI_service.drop(columns=["Unnamed: 0_level_0"])
    #PMI_service = PMI_service["Services PMI®"]
    df1 =  PMI_service["Unnamed: 0_level_0"]
    df2 =  PMI_service["Services PMI®"]
    PMI_service = pd.concat([df1, df2], axis=1)
    PMI_service["Series Index Jul"] = PMI_service["Series Index Jul"].astype(float)
    PMI_service["Series Index Jun"] = PMI_service["Series Index Jul"].astype(float)

    return PMI_manufacture,PMI_service

