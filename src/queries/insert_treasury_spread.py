import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.treasury_spread import get_treasury_spread

def insert_treasury_spread():
    configure_env()
    df = get_treasury_spread()
    save_to_postgres(df, "treasury_spread")

insert_treasury_spread()
