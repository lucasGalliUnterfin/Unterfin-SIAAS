import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.connection import fechaDelDia
from src.db.db_insert import save_to_postgres
from src.ingestion.cashFlow import get_cashFlow


fechaInicio = os.getenv("fechaInicio")
fechaFin = fechaDelDia()


def insert_cashFlow(fechaInicio,fechaFin):
    configure_env()
    df = get_cashFlow(fechaInicio,fechaFin)
    save_to_postgres(df, "Cash Flow")

insert_cashFlow(fechaInicio,fechaFin)

