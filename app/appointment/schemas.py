import datetime

from pydantic import BaseModel


class SAppointmentDetail(BaseModel):
    pet_id: int
    services: list[int]


class SAppointment(BaseModel):
    employee_id: int
    date: datetime.datetime
    details: list[SAppointmentDetail]
