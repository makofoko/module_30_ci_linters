import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from homework.celery_app import celery_app

# Настройки SMTP берём из переменных окружения
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Флаг: если True → только симуляция
SIMULATE_EMAIL = os.getenv("SIMULATE_EMAIL", "true").lower() == "true"


def send_email(order_id: str, receiver: str, filename: str):
    """Отправка письма с архивом или симуляция."""
    if SIMULATE_EMAIL:
        print(f"[SIMULATION] Email would be sent to {receiver} with {filename} for order {order_id}")
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email["Subject"] = f"Изображения. Заказ №{order_id}"
        email["From"] = SMTP_USER
        email["To"] = receiver

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filename)}")
        email.attach(part)

        server.sendmail(SMTP_USER, receiver, email.as_string())


@celery_app.task
def send_email_task(order_id: str, receiver: str, filename: str):
    """Celery-задача: отправка архива пользователю."""
    send_email(order_id, receiver, filename)
    return f"Email {'simulated' if SIMULATE_EMAIL else 'sent'} to {receiver} for order {order_id}"


@celery_app.task
def weekly_newsletter():
    """Celery-задача: еженедельная рассылка подписчикам."""
    if not os.path.exists("subscribers.txt"):
        return "No subscribers"

    with open("subscribers.txt", "r") as f:
        subscribers = [line.strip() for line in f.readlines()]

    for email in subscribers:
        if SIMULATE_EMAIL:
            print(f"[SIMULATION] Weekly newsletter sent to {email}")
        else:
            # можно сделать реальную отправку через SMTP
            print(f"[REAL] Weekly newsletter sent to {email}")

    return f"Newsletter {'simulated' if SIMULATE_EMAIL else 'sent'} to {len(subscribers)} subscribers"