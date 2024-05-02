from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic import BaseModel, EmailStr


class SEmployeeAdd(BaseModel):
    full_name: str
    phone: PhoneNumber
    email: EmailStr


class SEmployeeGet(SEmployeeAdd):
    id: int
