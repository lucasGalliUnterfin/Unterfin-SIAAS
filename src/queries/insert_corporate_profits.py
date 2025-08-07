import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.cp import get_CP
from src.db.connection import fechaDelDia

fechaInicio = os.getenv("fechaInicio")
fechaFin = fechaDelDia()

def insert_cp(fechaInicio,fechaFin):
    configure_env()
    df = get_CP(fechaInicio,fechaFin)
    save_to_postgres(df,"Corporate Profits")

insert_cp(fechaInicio,fechaFin)