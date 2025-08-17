from celery import Celery
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask import Flask

load_dotenv()

# Configuración Flask mínima para Mail
flask_app = Flask(__name__)
flask_app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS") == "True",
    MAIL_USE_SSL=False
)
mail = Mail(flask_app)

# Configuración Celery
celery = Celery(
    'tasks',
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

@celery.task
def send_email_async(subject, recipient, body):
    with flask_app.app_context():
        try:
            msg = Message(subject=subject, recipients=[recipient], body=body)
            mail.send(msg)
            return f"Correo enviado a {recipient}"
        except Exception as e:
            return f"Error enviando correo: {str(e)}"
