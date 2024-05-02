import pytest

from app.auth.auth import hash_password
from app.config import settings
from app.main import lifespan
from app.users.models import User  # noqa
from app.pets.models import Pet  # noqa
from app.appointment.models.appointment import Appointment  # noqa
from app.appointment.models.appointment_detail import AppointmentDetail  # noqa
from app.appointment.models.services_to_pets import ServicesToPets  # noqa
from app.services.models import Service  # noqa
from app.auth.models import Jwt  # noqa
from app.employee.models import Employee  # noqa
from app.database import Base, engine, get_async_session

from app.main import app as fastapi_app

from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
async def test_prepare_data_base():
    assert settings.MODE == "TEST"
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with get_async_session() as session:
        user = User(
            phone="tel:+7-888-999-88-99",
            email="admin@test.ru",
            full_name="Админ Админович Админов",
            hashed_password=hash_password("test"),
            is_admin=True,
        )
        session.add(user)
        await session.commit()
    yield


@pytest.fixture(scope="function")
async def ac():
    async with lifespan(fastapi_app):
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="https://test"
        ) as ac:
            yield ac


@pytest.fixture(scope="session")
async def admin_ac():
    async with lifespan(fastapi_app):
        async with AsyncClient(
            transport=ASGITransport(app=fastapi_app), base_url="https://test"
        ) as aca:

            r = await aca.post(
                url="/auth/login",
                data={
                    "login": "admin@test.ru",
                    "password": "test",
                },
            )
            assert r.status_code == 200
            assert aca.cookies["refresh_token"]
            assert aca.cookies["access_token"]

            yield aca
