import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.pmi import get_PMI

def insert_pmi():
    configure_env()
    dfM,dfS = get_PMI()
    save_to_postgres(dfM,"PMI Manufactura")
    save_to_postgres(dfS,"PMI Servicios")
    
insert_pmi()