from fastapi import HTTPException
from starlette import status


class BaseAuthException(HTTPException):
    status_code = 500
    detail = "На сервере произошла не предвиденная ошибка"

    def __init__(self, headers: dict | None = None):
        if headers is None:
            headers = {}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=headers
        )


class IncorrectJWTException(BaseAuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный токен"


class UnauthorizedException(BaseAuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не аутентифицированы"


class UserAlreadyExistException(BaseAuthException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким телефоном или email уже существует"


class IncorrectPasswordOrLoginException(BaseAuthException):
    status_code = 400
    detail = "Не верный Логин или Пароль"
