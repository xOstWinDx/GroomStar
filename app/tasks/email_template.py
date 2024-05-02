import datetime
from email.message import EmailMessage

from app.config import settings


def create_task_email_template(time: datetime.time, email_to):

    email = EmailMessage()
    email["Subject"] = "Напоминание"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""
                    <h1>Здравствуйте! это Зоосалон</h1>
                    <p>Напоминаем, у вас бронь сегодня на {time}</p>  
                """,
        subtype="html",
    )
    return email
