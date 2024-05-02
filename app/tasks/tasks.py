import asyncio
import datetime
import smtplib
from pathlib import Path

from PIL import Image
from celery import Celery
from celery.schedules import crontab

from app.appointment.dao import AppointmentDAO
from app.appointment.models.appointment import Appointment
from app.config import settings
from app.tasks.email_template import create_task_email_template

celery = Celery(
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    broker_connection_retry_on_startup=False,
)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=9, minute=30),
        email_notify.s(10),
    )
    sender.add_periodic_task(
        crontab(hour=11, minute=30),
        email_notify.s(12),
    )
    sender.add_periodic_task(
        crontab(hour=13, minute=30),
        email_notify.s(14),
    )
    sender.add_periodic_task(
        crontab(hour=15, minute=30),
        email_notify.s(16),
    )
    sender.add_periodic_task(
        crontab(hour=17, minute=30),
        email_notify.s(18),
    )
    # sender.add_periodic_task(
    #     crontab(minute="*/1"),
    #     email_notify.s(18),
    # )


def async2sync(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        task = loop.create_task(func(*args, **kwargs))
        task.add_done_callback(lambda f: loop.stop())
        loop.run_forever()
        try:
            return task.result()
        except asyncio.CancelledError:
            pass

    return wrapper


@celery.task()
@async2sync
async def email_notify(hour: int):
    date_now = datetime.datetime.now().date()
    date_time = datetime.datetime(
        date_now.year, date_now.month, date_now.day, hour=hour
    )
    appointments: list[dict[str, Appointment]] = await AppointmentDAO.fetch_all(
        date=date_time
    )
    emails: list = []
    for appointment in appointments:
        email = create_task_email_template(
            time=appointment["Appointment"].date.time(),
            email_to=appointment["Appointment"].customer.email,
        )
        emails.append(email)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        for email in emails:
            server.send_message(email)


@celery.task
def resize_photo(path: str):
    img_path = Path(path)
    im = Image.open(img_path)
    im_resized_500_250 = im.resize((500, 250))
    im_resized_500_250.save(f"app/static/services/resized_500_250_{img_path.name}")
