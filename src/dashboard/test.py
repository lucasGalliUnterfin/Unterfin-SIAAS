import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from src.db.connection import get_db_engine

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Alertas", layout="wide")

st.title("📊 Dashboard de Alertas Financieras")

# --- Conectar y leer datos ---
engine = get_db_engine()

query = """
SELECT a.id,
       a.date,
       a.title,
       a.description,
       a.url,
       s.severity AS severity_name
FROM alerts a
JOIN severities s ON a.severity = s.id;
"""
df = pd.read_sql(query, engine)

# --- Conversión de tipos ---
df["date"] = pd.to_datetime(df["date"])

# --- Filtros en sidebar ---
with st.sidebar:
    st.header("Filtros")
    severity_options = df["severity_name"].unique().tolist()
    severity_filter = st.multiselect(
        "Severidad",
        options=severity_options,
        default=severity_options
    )
    start_date = st.date_input("Fecha desde", df["date"].min().date())
    end_date = st.date_input("Fecha hasta", df["date"].max().date())

    # Adaptamos a timestamptz
    start_date_ts = pd.Timestamp(start_date).tz_localize("UTC")
    end_date_ts = pd.Timestamp(end_date).tz_localize("UTC")

# Aplicar filtros
df = df[df["severity_name"].isin(severity_filter)]
df = df[(df["date"] >= start_date_ts) & (df["date"] <= end_date_ts)]

# --- Métricas ---
col1, col2, col3 = st.columns(3)
col1.metric("🔴 Rojas", (df["severity_name"] == "rojo").sum())
col2.metric("🟡 Amarillas", (df["severity_name"] == "amarillo").sum())
col3.metric("🟢 Verdes", (df["severity_name"] == "verde").sum())

# --- Gráfico de distribución ---
severity_counts = df["severity_name"].value_counts().reset_index()
severity_counts.columns = ["severity", "count"]
fig = px.pie(
    severity_counts,
    values="count",
    names="severity",
    color="severity",
    color_discrete_map={"rojo": "#d9534f", "amarillo": "#f0ad4e", "verde": "#5cb85c"},
    title="Distribución de alertas"
)
st.plotly_chart(fig, use_container_width=True)

# --- Línea temporal ---
df_daily = df.groupby(["date", "severity_name"]).size().reset_index(name="count")
fig2 = px.line(
    df_daily,
    x="date",
    y="count",
    color="severity_name",
    color_discrete_map={"rojo": "#d9534f", "amarillo": "#f0ad4e", "verde": "#5cb85c"},
    title="Alertas por día"
)
st.plotly_chart(fig2, use_container_width=True)

# --- Tabla ---

SEVERITY_COLORS = {
    "rojo": "#e74c3c",
    "amarillo": "#f39c12",
    "verde": "#27ae60"
}

st.subheader("📋 Detalle de alertas")
for _, row in df.iterrows():
    color = SEVERITY_COLORS.get(row["severity_name"], "#7f8c8d")
    st.markdown(
        f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="margin-bottom: 5px;">
                <a href="{row['url']}" target="_blank" style="text-decoration: none; color: black;">
                    {row['title']}
                </a>
            </h3>
            <span style="color: {color}; font-weight: bold;">{row['severity_name'].capitalize()}</span>
            <p style="margin-top: 8px;">{row['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )