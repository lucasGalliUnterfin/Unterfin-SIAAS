import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.inflacion import get_inflacion

#Las fechas son totalmente aribitrias, las puse para testear
fechaInicio = "2024-06-01"
fechaFin = "2025-04-01"

def insert_inflacion(fechaInicio,fechaFin):
    configure_env()
    df = get_inflacion(fechaInicio,fechaFin)
    save_to_postgres(df,"Inflacion")

insert_inflacion(fechaInicio,fechaFin)