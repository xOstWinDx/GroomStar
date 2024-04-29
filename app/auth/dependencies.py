from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.params import Cookie
from jwt.exceptions import PyJWTError
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.auth.auth import set_pair_token
from app.auth.dao import JwtDAO
from app.auth.models import Jwt
from app.config import settings
from app.exceptions import IncorrectJWTException, UnauthorizedException
from app.users.dao import UserDAO
from app.users.models import User


async def decode_jwt(response, token):
    payload = None
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key_path.read_text(),
            settings.ALGORITHM,
        )
    except PyJWTError as e:
        await delete_token_cookie(response)
    return payload


async def delete_token_cookie(response: Response):
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    headers = {"set-cookie": response.headers["set-cookie"]}
    raise IncorrectJWTException(headers)


async def validate_jwt(db_token, response: Response, request: Request, payload):

    if db_token is None:
        await delete_token_cookie(response)
    if not db_token.is_active:
        await delete_token_cookie(response)
    if db_token.ip_address != request.client.host:
        await JwtDAO.update(payload.get("jti"), False)
        await delete_token_cookie(response)
    if db_token.user_agent != request.headers.get("user-agent"):
        await JwtDAO.delete(id=payload.get("jti"))


async def get_token(
    request: Request,
    response: Response,
    access_token: Annotated[str | None, Cookie(include_in_schema=False)] = None,
    refresh_token: Annotated[str | None, Cookie(include_in_schema=False)] = None,
):
    if access_token is None:
        if refresh_token is None:
            raise UnauthorizedException()
        payload = await decode_jwt(response, refresh_token)

        db_token: Jwt = await JwtDAO.fetch_one_or_none(id=payload.get("jti"))

        await validate_jwt(db_token, response, request, payload)

        access_token = await set_pair_token(
            request.headers.get("user-agent"),
            request.client.host,
            payload.get("sub", None),
            response,
        )
        access_token = access_token[0]
        await JwtDAO.delete(id=payload.get("jti"))

    return access_token


async def get_current_user(response: Response, token: str = Depends(get_token)) -> User:
    payload = await decode_jwt(response, token)
    user_id = payload.get("sub", None)
    if user_id is None:
        await delete_token_cookie(response)

    user = await UserDAO.fetch_one_or_none(id=user_id)
    if user is None:
        await delete_token_cookie(response)

    return user


async def get_current_user_admin(user=Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет доступа"
        )
    return user
