import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.order(4)
class TestAppointment:
    @pytest.mark.parametrize(
        "employee_id, date, details, status_code",
        [
            (
                1,
                "2024-05-02T18:00:00.000",
                [{"pet_id": 1, "services": [1, 2, 3]}],
                201,
            ),
            (
                2,
                "2024-05-02T18:00:00.000",
                [
                    {"pet_id": 1, "services": [1, 2, 3]},
                    {"pet_id": 2, "services": [1, 2, 3]},
                ],
                201,
            ),
            (
                2,
                "2024-05-02T18:00:00.000",
                [{"pet_id": 1, "services": [1, 2, 3]}],
                409,
            ),
        ],
    )
    async def test_appointment_add(
        self, employee_id, date, details, status_code, admin_ac: AsyncClient
    ):
        response = await admin_ac.post(
            "/appointment/add",
            json={
                "employee_id": employee_id,
                "date": date,
                "details": details,
            },
        )
        print(response.json())
        assert response.status_code == status_code

    async def test_appointment_get(self, admin_ac: AsyncClient):
        response = await admin_ac.get(
            "/appointment/get",
        )
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) == 2
