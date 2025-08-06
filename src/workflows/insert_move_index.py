import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres
from src.ingestion.move_index import get_move_index

def insert_move_index():
    configure_env()
    df = get_move_index()
    save_to_postgres(df, "move_index")

insert_move_index()
