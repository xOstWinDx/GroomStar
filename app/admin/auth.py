from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.auth.auth import auth_user, create_token, set_pair_token
from app.auth.dependencies import (
    get_current_user_admin,
    get_current_user,
    get_token,
    decode_jwt,
)
from app.users.schemas import SUserLogin


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user_data = SUserLogin(login=email, password=password)
        user = await auth_user(user_data)
        access_token = await create_token(
            request.headers["user-agent"], request.client.host, user.id, "access"
        )

        request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session

        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        payload = await decode_jwt(None, token)
        user = await get_current_user(None, payload)
        if user.is_admin:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет доступа"
        )
