from dataclasses import dataclass

from fastapi import Form
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import PydanticCustomError
from pydantic_extra_types.phone_numbers import PhoneNumber


@dataclass
class SUserGet:
    phone: PhoneNumber = Form()
    email: EmailStr = Form()
    name: str = Form()


@dataclass
class SUserReg(SUserGet):

    password: str = Form()

    def as_dict(self):
        return {
            "phone": self.phone,
            "email": self.email,
            "full_name": self.name,
            "hashed_password": self.password,
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
