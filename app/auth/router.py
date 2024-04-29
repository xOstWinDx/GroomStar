from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import Response

from app.auth.auth import (
    validate_user_data,
    auth_user,
    hash_password,
    set_pair_token,
)
from app.users.dao import UserDAO
from app.users.models import User
from app.users.schemas import SUserReg, SUserLogin

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=201)
async def register_user(user_data=Depends(validate_user_data)):
    user_dict = user_data.as_dict()
    user_dict["hashed_password"] = hash_password(user_dict["hashed_password"])
    user: User = await UserDAO.add(**user_dict)

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect Data")


@router.post("/login", status_code=200)
async def login_user(
    request: Request, response: Response, user_data: SUserLogin = Depends()
):
    if request.cookies.get("refresh_token"):
        raise HTTPException(status_code=400, detail="Вы уже аутентифицированы")
    user: User = await auth_user(user_data)
    await set_pair_token(
        request.headers.get("user-agent"), request.client.host, user.id, response
    )


@router.post("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
