import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import pandas as pd
from src.db.connection import configure_env
from src.db.db_insert import save_to_postgres

def insert_alerts(df: pd.DataFrame):
    configure_env()
    save_to_postgres(df, "alerts", if_exists="append")