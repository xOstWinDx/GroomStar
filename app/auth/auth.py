from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import User
from app.users.schemas import SUserReg, SUserLogin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def validate_user_data(user_data: SUserReg = Depends()):
    user = await UserDAO.fetch_one_or_none(phone=user_data.phone)
    if user is not None:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким телефоном уже существует"
        )
    user = await UserDAO.fetch_one_or_none(email=user_data.email)
    if user is not None:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким Email уже существует"
        )
    return user_data


def hash_password(password: str) -> str:
    print(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User):
    payload = {"sub": user.id, "exp": datetime.now() + timedelta(minutes=15)}
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token


async def auth_user(user_data: SUserLogin):
    user_dict = user_data.as_dict()
    password = user_dict.pop("hashed_password")
    user: User = await UserDAO.fetch_one_or_none(**user_dict)
    if user is None:
        raise HTTPException(status_code=400, detail="Не верный Email или Пароль")

    if verify_password(
        password,
        user.hashed_password,
    ):
        return user

    raise HTTPException(status_code=400, detail="Не верный Email или Пароль")
