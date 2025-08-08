import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Configuración
def get_db_engine():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'claves.env'))
    user = os.getenv("SUPABASE_USER")
    password = os.getenv("SUPABASE_PASSWORD")
    host = os.getenv("SUPABASE_HOST")
    port = os.getenv("SUPABASE_PORT")
    db = os.getenv("SUPABASE_DB")

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?sslmode=require"
    return create_engine(conn_str)

# Consultar datos de una tabla
def query_table(table_name: str):
    engine = get_db_engine()
    with engine.connect() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    return df

# df = query_table("severities")   # 👈 cambiar por la tabla a consultar
# print(df)
