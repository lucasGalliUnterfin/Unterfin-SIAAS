import os
import re
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

SEVERITY_EMOJI = {
    "1": ":red_circle: Severidad roja",
    "2": ":large_yellow_circle: Severidad amarilla",
    "3": ":large_green_circle: Severidad verde"
}


def send_alert(message: str, channel: str = "#testing-botalertas"):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=message
        )
        #print("✅ Mensaje enviado:", response["ts"])
    except SlackApiError as e:
        print("❌ Error al enviar mensaje:", e.response["error"])

def clean_html(text: str) -> str:
    """Elimina etiquetas HTML de un string."""
    return re.sub(r'<[^>]+>', '', text)

def send_alert_block(title: str, description: str, url: str, severity: str, channel: str = "#testing-botalertas"):
    try:
        emoji_label = SEVERITY_EMOJI.get(str(severity), "🔘 Severidad sin clasificar")

        clean_desc = clean_html(description).strip()
        clean_title = clean_html(title).strip()

        # Para las URL de tradingeconomics, aseguramos que comiencen con https
        if not url.startswith("http"):
            url = "https://tradingeconomics.com" + url

        full_title = f"<{url}|{clean_title}>"

        response = client.chat_postMessage(
            channel=channel,
            text=f"[{emoji_label}] {clean_title} - {url}",  # Para notificaciones accesibles
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{emoji_label}*\n{full_title}\n{clean_desc}"
                    }
                }
            ]
        )
    except SlackApiError as e:
        print("❌ Error al enviar mensaje enriquecido:", e.response["error"])




#if __name__ == "__main__":
#    send_alert("Racing goleó 3-0 a Riestra :smile:")
