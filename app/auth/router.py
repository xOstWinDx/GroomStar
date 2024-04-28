from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import Response

from app.auth.auth import (
    validate_user_data,
    auth_user,
    create_access_token,
    hash_password,
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
async def login_user(response: Response, user_data: SUserLogin = Depends()):
    user: User = await auth_user(user_data)
    response.set_cookie(
        key="token",
        value=create_access_token(user),
        max_age=900,
        secure=True,
        httponly=True,
    )


@router.post("/logout", status_code=200)
async def logout_user(response: Response):
    response.delete_cookie("token")
