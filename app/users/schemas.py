from dataclasses import dataclass

from fastapi import Form
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic_core import PydanticCustomError
from pydantic_extra_types.phone_numbers import PhoneNumber


class SUserGet(BaseModel):
    phone: PhoneNumber = Form()
    email: EmailStr = Form()
    full_name: str = Form()
    model_config = ConfigDict(from_attributes=True)


@dataclass
class SUserReg:

    phone: PhoneNumber = Form()
    email: EmailStr = Form()
    full_name: str = Form()
    password: str = Form()

    def as_dict(self):
        return {
            "phone": self.phone.strip(),
            "email": self.email.strip(),
            "full_name": self.full_name.strip(),
            "hashed_password": self.password.strip(),
        }


@dataclass
class SUserLogin:
    login: PhoneNumber | EmailStr = Form()
    password: str = Form()

    def as_dict(self):
        try:
            PhoneNumber._validate(self.login, None)
            return {
                "phone": self.login,
                "hashed_password": self.password,
            }
        except PydanticCustomError:
            return {
                "email": self.login,
                "hashed_password": self.password,
            }
