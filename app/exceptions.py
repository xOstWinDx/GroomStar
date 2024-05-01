from fastapi import HTTPException
from starlette import status


class BaseApiException(HTTPException):
    status_code = 500
    detail = "На сервере произошла не предвиденная ошибка"

    def __init__(self, headers: dict | None = None):
        if headers is None:
            headers = {}
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=headers
        )


class IncorrectJWTException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный токен"


class UnauthorizedException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Вы не аутентифицированы"


class UserAlreadyExistException(BaseApiException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким телефоном или email уже существует"


class IncorrectPasswordOrLoginException(BaseApiException):
    status_code = 400
    detail = "Неверный Логин или Пароль"


class IncorrectIDException(BaseApiException):
    status_code = 400
    detail = "Неверный  айди"
