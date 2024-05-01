import datetime
from datetime import time
import re

from fastapi import HTTPException
from fastapi.openapi.models import Response

from app.appointment.dao import AppointmentDAO
from app.appointment.schemas import SAppointment
from app.employee.dao import EmployeeDAO
from app.services.dao import ServicesDAO
from app.users.models import User


async def validate_pets(user, appo_data: SAppointment, response):
    user_pets = [pet.id for pet in user.pets]
    for detail in appo_data.details:
        if detail.pet_id not in user_pets:
            raise HTTPException(
                status_code=400,
                detail=f"У вас нет питомца с айди {detail.pet_id}",
                headers=response.headers,
            )
    return True


async def validate_employee(appo_data: SAppointment, response):
    employees_id = await EmployeeDAO.get_all_ids()
    if appo_data.employee_id not in employees_id:
        raise HTTPException(
            status_code=400,
            detail=f"У нас нет работника с айди {appo_data.employee_id}",
            headers=response.headers,
        )
    return True


async def validate_date(appo_data: SAppointment, response):
    if (
        appo_data.date.time() != time(10)
        and appo_data.date.time() != time(12)
        and appo_data.date.time() != time(14)
        and appo_data.date.time() != time(16)
        and appo_data.date.time() != time(18)
    ):
        raise HTTPException(
            status_code=400,
            detail=f"Бронь осуществляется только на 10 12 14 16 и 18 часов",
            headers=response.headers,
        )
    date_list: list = await AppointmentDAO.get_date_of_employees(
        appo_data.date, appo_data.employee_id
    )
    if appo_data.date in date_list:
        raise HTTPException(
            status_code=400,
            detail=f"Это время уже занято",
            headers=response.headers,
        )

    return True


async def validate_services(appo_data: SAppointment, response):
    services_list = set(await ServicesDAO.get_all_ids())
    for detail in appo_data.details:
        if not services_list.issubset(set(detail.services)):
            raise HTTPException(
                status_code=400,
                detail=f"У нас нет услуг с таким ID",
                headers=response.headers,
            )


async def validate_appoint(response: Response, user: User, appo_data: SAppointment):
    print(response.headers)
    await validate_pets(user, appo_data, response)
    await validate_services(appo_data, response)
    await validate_employee(appo_data, response)
    await validate_date(appo_data, response)
