from pydantic import BaseModel


class SEmployeeAdd(BaseModel):
    full_name: str
    phone: str
    email: str


class SEmployeeGet(SEmployeeAdd):
    id: int
