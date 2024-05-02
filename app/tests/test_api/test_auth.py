import pytest
from httpx import AsyncClient


class TestAuth:
    @pytest.mark.parametrize(
        "phone, email, full_name, password, status_code",
        [
            ("+79999999999", "test@test.com", "Json Mamoa", "test", 201),
            ("+79999999999", "test@test.com", "Json Mamoa", "test", 409),
            (1234, "test@test.com", "Json Mamoa", "test", 422),
            ("+7ddfgfdg", "test@test.com", "Json Mamoa", "test", 422),
            ("+78888888888", "test.com", "Json Mamoa", "test", 422),
        ],
    )
    async def test_register(
        self, phone, email, full_name, password, status_code, ac: AsyncClient
    ):
        response = await ac.post(
            "/auth/register",
            data={
                "phone": phone,
                "email": email,
                "full_name": full_name,
                "password": password,
            },
        )
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "login, password, status_code",
        [
            ("+79999999999", "test", 200),
            ("test@test.com", "test", 200),
            (1234, "test", 422),
            ("+7ddfgfdg", "test", 422),
            ("+78888888888", "test", 422),
        ],
    )
    async def test_login(self, login, password, status_code, ac: AsyncClient):
        response = await ac.post(
            "/auth/login",
            data={
                "login": login,
                "password": password,
            },
        )
        assert response.status_code == status_code
