import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.EPS import get_epsInd


"""

NO CORRER hay que sortear unos temas con yfinance

"""

def insert_eps(n = 100):
    configure_env()
    df,_ = get_epsInd(n)
    save_to_postgres(df,"EPS")

insert_eps()