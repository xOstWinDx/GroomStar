import pytest
from httpx import AsyncClient


@pytest.mark.order(1)
class TestEmployee:

    @pytest.mark.parametrize(
        "full_name, phone, email, status_code",
        [
            ("Rabotnik1", "+79818129821", "rabotnik1@yandex.ru", 201),
            ("Rabotnik2", "+79818129822", "rabotnik2@yandex.ru", 201),
            ("Rabotnik3", "+79818129823", "rabotnik3@yandex.ru", 201),
            ("Rabotnik4", "+79818129824", "rabotnik4@yandex.ru", 201),
            ("Rabotnik4", "+79818129824", "rabotnik4@yandex.ru", 409),
            ("Rabotnik6", "zzzz", "rabotnik6@yandex.ru", 422),
            ("Rabotnik7", "79818129825", "rabotnik4", 422),
        ],
    )
    async def test_add_employee(
        self, full_name, phone, email, status_code, admin_ac: AsyncClient
    ):
        response = await admin_ac.post(
            "/employees/add",
            json={
                "full_name": full_name,
                "phone": phone,
                "email": email,
            },
        )

        assert response.status_code == status_code

    async def test_get_employee(self, admin_ac: AsyncClient):
        response = await admin_ac.get("/employees/get")

        assert response.status_code == 200
        assert len(response.json()) == 4
