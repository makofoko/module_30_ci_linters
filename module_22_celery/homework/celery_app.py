from celery import Celery
import os
from celery.schedules import crontab

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "homework",
    broker=broker_url,
    backend=result_backend,
    include=["homework.image", "homework.mail"]
)

# Настройка Celery Beat для еженедельной рассылки
celery_app.conf.beat_schedule = {
    "weekly-newsletter": {
        "task": "homework.mail.weekly_newsletter",
        # каждую неделю в понедельник в 9:00 утра
        "schedule": crontab(hour=9, minute=0, day_of_week="monday"),
    }
}

celery_app.conf.timezone = "UTC"
