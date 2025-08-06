import tradingeconomics as te
import os
from dotenv import load_dotenv

#### ! Disclaimer: estamos con el plan gratis

load_dotenv()
TE_KEY = os.getenv("TE_KEY")

def get_calendar_data():
    # Hacer login
    te.login(TE_KEY)

    # Obtener calendario de eventos
    calendar = te.getCalendarData()
    print(calendar[:5])


get_calendar_data()


### Investigar para el futuro: te.suscribe(['calendar', 'news', 'markets'])

