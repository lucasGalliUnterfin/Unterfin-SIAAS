import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv("claves.env")

def configure_env():
    load_dotenv("claves.env")

def get_db_engine():
    user = os.getenv("SUPABASE_USER")
    password = os.getenv("SUPABASE_PASSWORD")
    host = os.getenv("SUPABASE_HOST")
    port = os.getenv("SUPABASE_PORT")
    db = os.getenv("SUPABASE_DB")

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?sslmode=require"
    return create_engine(conn_str)
