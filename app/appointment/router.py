from typing import Annotated

from fastapi import APIRouter, Depends, Query, HTTPException
from starlette.responses import Response

from app.appointment.appointment_validate import (
    validate_pets,
    validate_employee,
    validate_date,
    validate_services,
    validate_appoint,
)
from app.appointment.dao import AppointmentDAO
from app.appointment.schemas import SAppointment
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/appointment", tags=["appointment"])


@router.post("/add")
async def add_appointment(
    response: Response, appo_data: SAppointment, user=Depends(get_current_user)
):
    await validate_appoint(response, user, appo_data)
    appo_dict = appo_data.model_dump()
    appo_dict["customer_id"] = user.id
    await AppointmentDAO.add(**appo_dict)


@router.get("/get")
async def get_appointment(user=Depends(get_current_user)):
    return await AppointmentDAO.fetch_all(customer_id=user.id)
