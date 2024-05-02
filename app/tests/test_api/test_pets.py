import pytest
from httpx import AsyncClient


@pytest.mark.order(2)
class TestPets:
    @pytest.mark.parametrize(
        "name, species, breed, status_code",
        [
            ("Мила", "Собака", "Йорк", 201),
            ("Лина", "Собака", "Шпиц", 201),
            ("Аска", "Хомяк", "Джунгарик", 422),
            ("Аска", "Другое", "Джунгарик", 201),
        ],
    )
    async def test_pet_add(
        self, name, species, breed, status_code, admin_ac: AsyncClient
    ):
        response = await admin_ac.post(
            "/pets/add",
            json={
                "name": name,
                "species": species,
                "breed": breed,
            },
        )
        assert response.status_code == status_code

    async def test_pet_get(self, admin_ac: AsyncClient):
        response = await admin_ac.get("/pets/get")
        assert response.status_code == 200
        assert len(response.json()) == 3
