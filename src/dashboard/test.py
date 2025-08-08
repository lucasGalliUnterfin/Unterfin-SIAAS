# Se corre con streamlit run c:/Users/resea/OneDrive/Escritorio/Unterfin-SIAAS/src/dashboard/test.py

# Se corre con streamlit run c:/Users/resea/OneDrive/Escritorio/Unterfin-SIAAS/src/dashboard/test.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import pytz
from datetime import date
from sqlalchemy import text

from src.db.connection import get_db_engine

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard de Alertas Financiera - Unterfin", layout="wide")

st.title("📊 Dashboard de Alertas Financiera - Unterfin")

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

# Aplicar filtros básicos (severidad + sidebar fechas)
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

############## Buscador ###############################
# --- Controles de filtrado ---
col_buscar, col_fecha1, col_fecha2, col_orden = st.columns([3, 2, 2, 2])

with col_buscar:
    filtro_texto = st.text_input("🔍 Buscar", "")

with col_fecha1:
    fecha_inicio = st.date_input("Desde", value=df["date"].min().date())

with col_fecha2:
    fecha_fin = st.date_input("Hasta", value=df["date"].max().date())

with col_orden:
    orden = st.selectbox("Ordenar por fecha", ["Más reciente", "Más antigua"])

# --- Aplicar filtros adicionales sobre df_filtrado (que parte del df ya filtrado) ---
utc = pytz.UTC
df_filtrado = df.copy()

# Pasamos las fechas de inicio de fin a timestamptz
fecha_inicio_ts = pd.Timestamp(fecha_inicio).tz_localize(utc)
fecha_fin_ts = pd.Timestamp(fecha_fin).tz_localize(utc) + pd.Timedelta(days=1)

if filtro_texto:
    df_filtrado = df_filtrado[
        df_filtrado["title"].str.contains(filtro_texto, case=False, na=False) |
        df_filtrado["description"].str.contains(filtro_texto, case=False, na=False)
    ]

# Aplicamos las fechas al df_filtrado
df_filtrado = df_filtrado[
    (df_filtrado["date"] >= fecha_inicio_ts) &
    (df_filtrado["date"] <= fecha_fin_ts)
]

if orden == "Más reciente":
    df_filtrado = df_filtrado.sort_values("date", ascending=False)
else:
    df_filtrado = df_filtrado.sort_values("date", ascending=True)


############## Sistema de mejora de las recomendaciones ###################

def update_severity_boss(alert_id, new_severity_name):
    engine = get_db_engine()
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE alerts
                SET severity_boss = (
                    SELECT id FROM severities WHERE severity = :sev
                )
                WHERE id = :alert_id
            """),
            {"sev": new_severity_name, "alert_id": alert_id}
        )

SEVERITY_OPTIONS = ["rojo", "amarillo", "verde", "no es alerta"]

SEVERITY_COLORS = {
    "rojo": "#e74c3c",
    "amarillo": "#f39c12",
    "verde": "#27ae60",
    "no es alerta": "#7f8c8d"
}

SEVERITY_MAP = {
    "verde": 1,
    "amarillo": 2,
    "rojo": 3,
    "no es alerta": 4
}

st.subheader("📋 Detalle de alertas")

tabs = st.tabs(["🔴 Rojas", "🟡 Amarillas", "🟢 Verdes", "📋 Todas"])
severities_tab_map = {
    0: "rojo",
    1: "amarillo",
    2: "verde",
    3: None
}

for i, tab in enumerate(tabs):
    with tab:
        filtro = severities_tab_map[i]
        
        if filtro:
            df_filtered = df_filtrado[df_filtrado["severity_name"] == filtro]
        else:
            df_filtered = df_filtrado.copy()

        for _, row in df_filtered.iterrows():
            color = SEVERITY_COLORS.get(row["severity_name"], "#7f8c8d")

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 10px;
                                box-shadow: 0 2px 5px rgba(0,0,0,0.05); position: relative;">
                        <h3 style="margin-bottom: 5px;">
                            <a href="{row['url']}" target="_blank" style="text-decoration: none; color: black;">
                                {row['title']}
                            </a>
                        </h3>
                        <span style="background-color:{color}; color: white; padding: 3px 8px; border-radius: 5px; font-size: 0.8rem;">
                            {row['severity_name'].capitalize() if row['severity_name'] else "—"}
                        </span>
                        <p style="margin-top: 8px; color:#555;">
                            { (row['description'][:180] + '...') if row['description'] and len(row['description'])>180 else (row['description'] or '') }
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with col2:
                with st.popover("⋮"):
                    st.write("Sugerir cambio de color de alerta:")
                    for name in SEVERITY_MAP.keys():
                        btn_label = name.capitalize()
                        # Label del boton
                        if st.button(
                            f"⬤ {btn_label}",
                            key=f"{name}_{row['id']}_tab{i}"
                        ):
                            if update_severity_boss(row['id'], name):
                                st.toast(f"✅ Cambiado a {btn_label}")
                                st.experimental_rerun()
