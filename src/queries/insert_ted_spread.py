import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.ted_spread import get_ted_spread

def insert_ted_spread():
    configure_env()
    df = get_ted_spread()
    save_to_postgres(df, "ted_spread")

insert_ted_spread()
