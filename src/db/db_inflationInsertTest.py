import pandas as pd
from connection import get_db_engine
from indicadoresLideresSrc import get_inflation

def save_to_postgres(df: pd.DataFrame, table_name: str, if_exists="replace"):
    engine = get_db_engine()
    df.to_sql(table_name, engine, if_exists=if_exists, index=True, index_label="date")
    print(f"✅ Datos guardados en la tabla '{table_name}'")

fechaInicio = "2025-01-01"
fechaFin = "2025-04-01"

df = get_inflation(fechaInicio,fechaFin)

save_to_postgres(df,"Inflacion")