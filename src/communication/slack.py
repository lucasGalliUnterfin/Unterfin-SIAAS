import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Cargar variables desde el .env que está en la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../..", "claves.env"))

# Leer el token
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    raise ValueError("No se encontró la variable SLACK_BOT_TOKEN en claves.env")

# Inicializar cliente
client = WebClient(token=slack_token)

def send_alert(message: str, channel: str = "#testing-botalertas"):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        #print("✅ Mensaje enviado:", response["ts"])
    except SlackApiError as e:
        print("❌ Error al enviar mensaje:", e.response["error"])


#if __name__ == "__main__":
#    send_alert("Racing goleó 3-0 a Riestra :smile:")
