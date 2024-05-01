import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_extra_types.pendulum_dt import DateTime


class SAppointmentDetail(BaseModel):
    pet_id: int
    services: list[int]


class SAppointment(BaseModel):
    employee_id: int
    date: datetime.datetime
    details: list[SAppointmentDetail]
