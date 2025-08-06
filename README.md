# Sistema Inteligente de Alertas para Activos Globales

## Objetivo
Diseñar e implementar un sistema automatizado, que, mediante IA y análisis de datos, genere alertas tempranas sobre eventos macroeconómicos, microeconómicos y geopolíticos que impacten en la toma de decisiones de inversión global.

## Estructura de las carpetas actual
```
sistema_alertas_ai/
│── data/             # Datos crudos 
│── notebooks/        # Jupyter notebooks para pruebas rápidas
│── src/              # Código fuente principal
│   ├── ingestion/    # scripts para bajar datos
│   ├── db/           # conexión y queries a PostgreSQL
│   └── alerts/       # motor de reglas y notificaciones
│── tests/            # pruebas 
│── .env              # claves y credenciales
│── requirements.txt  # librerías del proyecto
│── README.md         # guía rápida del proyecto
```

## Base de datos

### Tablas 
Treasury Spread 
* date
* 2Y
* 10Y
* spread_2s10s

MOVE Index
* date
* move_index

