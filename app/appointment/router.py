from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.appointment.dao import AppointmentDAO
from app.appointment.schemas import SAppointment
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/appointment", tags=["appointment"])


@router.post("/add")
async def add_appointment(appo_data: SAppointment, user=Depends(get_current_user)):
    appo_dict = appo_data.model_dump()
    appo_dict["customer_id"] = user.id
    await AppointmentDAO.add(**appo_dict)


@router.get("/get")
async def get_appointment(user=Depends(get_current_user)):
    return await AppointmentDAO.fetch_all(customer_id=user.id)
