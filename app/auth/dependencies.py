from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.params import Cookie
from starlette import status
from starlette.requests import Request
from jwt.exceptions import PyJWTError

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import User


async def get_token(
    token: Annotated[str | None, Cookie(include_in_schema=False)] = None
):
    if token is None:
        raise HTTPException(status_code=400, detail="Невалидный токен")
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except PyJWTError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен"
        )
    user_id = payload.get("sub", None)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен"
        )
    user = await UserDAO.fetch_one_or_none(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный токен"
        )

    return user


async def get_current_user_admin(user=Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет доступа"
        )
    return user
