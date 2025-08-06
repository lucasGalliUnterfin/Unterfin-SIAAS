import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.sofr import get_sofr

def insert_sofr():
    configure_env()
    df = get_sofr()
    save_to_postgres(df, "sofr")

insert_sofr()
