from sqladmin import ModelView

from app.appointment.models.appointment import Appointment
from app.employee.models import Employee
from app.pets.models import Pet
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_details_list = [User.id, User.email, User.pets, User.appointments]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-sharp fa-solid fa-users"


class AppointmentAdmin(ModelView, model=Appointment):
    column_list = [c.name for c in Appointment.__table__.c] + [
        Appointment.details,
        Appointment.customer,
    ]
    column_details_list = [
        Appointment.id,
        Appointment.details,
        Appointment.customer,
        Appointment.employee_id,
    ]
    can_delete = True
    name = "Запись"
    name_plural = "Записи"
    icon = "fa-sharp fa-solid fa-list-check"


class PetAdmin(ModelView, model=Pet):
    column_list = [Pet.id, Pet.name] + [Pet.user]
    column_details_list = [Pet.id, Pet.name, Pet.user, Pet.species, Pet.breed]
    can_delete = True
    name = "Питомец"
    name_plural = "Питомцы"
    icon = "fa-solid fa-paw"


class EmployeeAdmin(ModelView, model=Employee):
    column_list = [Employee.id, Employee.full_name]
    column_details_list = [
        Employee.id,
        Employee.email,
        Employee.full_name,
        Employee.appointments,
    ]
    can_delete = True
    name = "Сотрудник"
    name_plural = "Сотрудники"
    icon = "fa-solid fa-address-card"
