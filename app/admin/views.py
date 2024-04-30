from sqladmin import ModelView

from app.appointment.models.appointment import Appointment
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_list = [User.id, User.email, User.pets, User.appointment]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-sharp fa-solid fa-users"


class AppointmentAdmin(ModelView, model=Appointment):
    column_list = [c.name for c in Appointment.__table__.c] + [
        Appointment.details,
        Appointment.customer,
    ]
    column_details_list = [User.id, User.email, User.pets, User.appointment]
    can_delete = False
    name = "Запись"
    name_plural = "Записи"
    icon = "fa-sharp fa-solid fa-list-check"
