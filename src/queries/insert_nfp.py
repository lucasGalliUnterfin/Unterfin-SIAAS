
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.connection import fechaDelDia
from src.db.db_insert import save_to_postgres
from src.ingestion.nfp import get_NFP

fechaInicio = os.getenv("fechaInicio")
fechaFin = fechaDelDia()

def insert_nfp(fechaInicio,fechaFin):
        configure_env()
        df = get_NFP(fechaInicio,fechaFin)
        save_to_postgres(df,"Non-farm Payroll")
        
insert_nfp(fechaInicio,fechaFin)