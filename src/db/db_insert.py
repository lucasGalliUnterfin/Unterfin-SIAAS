import pandas as pd
from src.db.connection import get_db_engine

def save_to_postgres(df: pd.DataFrame, table_name: str, if_exists="replace"):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=True, index_label="date")
    print(f"✅ Datos guardados en la tabla '{table_name}'")
