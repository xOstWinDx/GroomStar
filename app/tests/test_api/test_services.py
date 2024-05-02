import pytest
from httpx import AsyncClient


@pytest.mark.order(3)
class TestServices:
    @pytest.mark.parametrize(
        "title, description, price_small, price_big, status_code",
        [
            ("Стрижка", "Комплексная стрижка", 2500, 3500, 201),
            ("Гигиена", "Чистка ушей, чистка зубов", 1000, 2000, 201),
            ("Вычес", "Вычёсывание", 2000, 4000, 201),
            (123, 321, 1234, 2313, 422),
        ],
    )
    async def test_services_add(
        self,
        title,
        description,
        price_small,
        price_big,
        status_code,
        admin_ac: AsyncClient,
    ):
        response = await admin_ac.post(
            "/services/add",
            json={
                "title": title,
                "description": description,
                "price_small": price_small,
                "price_big": price_big,
            },
        )
        assert response.status_code == status_code

    async def test_services_get(self, admin_ac: AsyncClient):
        response = await admin_ac.get("/services/get")
        assert response.status_code == 200
        assert len(response.json()) == 3
