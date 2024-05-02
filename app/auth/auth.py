import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, Depends
from starlette.responses import Response

from app.auth.dao import JwtDAO
from app.config import settings
from app.exceptions import (
    UserAlreadyExistException,
    BaseApiException,
    IncorrectPasswordOrLoginException,
)
from app.users.dao import UserDAO
from app.users.models import User
from app.users.schemas import SUserReg, SUserLogin


async def validate_user_data(user_data: SUserReg = Depends()):
    user_data.email = user_data.email.lower()
    user = await UserDAO.fetch_one_or_none(phone=user_data.phone)
    if user is not None:
        raise UserAlreadyExistException()
    user = await UserDAO.fetch_one_or_none(email=user_data.email)
    if user is not None:
        raise UserAlreadyExistException()

    return user_data


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def set_pair_token(
    user_agent, ip_address, user_id, response: Response
) -> tuple[str, str]:
    try:
        access_token = await create_token(user_agent, ip_address, user_id, "access")
        refresh_token = await create_token(user_agent, ip_address, user_id, "refresh")
        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=900,
            httponly=True,
            secure=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=604_800,
            httponly=True,
            secure=True,
        )
        return access_token, refresh_token

    except Exception as e:
        print(e.args)
        raise BaseApiException()


def verify_password(plain_password: bytes, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)


async def create_token(user_agent, ip_address, user_id: int, token_type: str) -> str:
    if token_type == "refresh":
        exp = datetime.now() + timedelta(days=7)
        payload = {"sub": user_id, "exp": exp, "jti": str(uuid.uuid4())}
        await JwtDAO.add(
            id=payload["jti"],
            is_active=True,
            user_id=payload["sub"],
            ip_address=ip_address,
            user_agent=user_agent,
        )
    else:
        exp = datetime.now() + timedelta(minutes=10)
        payload = {"sub": user_id, "exp": exp}

    token = jwt.encode(
        payload, settings.auth_jwt.private_key_path.read_text(), settings.ALGORITHM
    )
    return token


async def auth_user(user_data: SUserLogin):
    user_data.login = user_data.login.lower()
    user_dict = user_data.as_dict()
    password = user_dict.pop("hashed_password").encode()
    user: User = await UserDAO.fetch_one_or_none(**user_dict)
    if user is None:
        raise IncorrectPasswordOrLoginException()
    if verify_password(
        password,
        user.hashed_password,
    ):
        return user
    raise IncorrectPasswordOrLoginException()
