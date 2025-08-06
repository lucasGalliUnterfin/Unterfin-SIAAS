import os
import smtplib
import ssl
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../..", "claves.env"))

def send_mail(subject, body, to_email=None):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 465))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    to_email = to_email or os.getenv("ALERTS_EMAIL")

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, msg.as_string())

send_mail("Testeo mail desde Python", "eso que dice el titulo")