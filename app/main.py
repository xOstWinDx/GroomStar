import asyncio
import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_async_session
from app.customers.models import Customer
from app.pets.models import Pet
from app.employees.models import Employee
from app.services.models import Service
from app.appointment.models.appointment import Appointment
from app.appointment.models.appointment_detail import AppointmentDetail
from app.appointment.models.services_to_pets import ServicesToPets

from app.database import engine, Base


async def fake_db_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with get_async_session() as session:
        cus1 = Customer(
            phone="+79675901769",
            email="starkatya0@yandex.ru",
            full_name="Старобогатов Алексей",
            hashed_password="123456",
        )

        pet1 = Pet(
            customer_id=1,
            name="Лина",
            species="Собака",
            breed="Шпиц",
        )

        pet2 = Pet(
            customer_id=1,
            name="Мила",
            species="Собака",
            breed="Йорк",
        )

        eml1 = Employee(
            phone="+79818118912",
            email="starka0@yandex.ru",
            full_name="Старобогатова Екатерина",
            hashed_password="123456",
            post="Хозяйка",
        )

        serv1 = Service(
            title="Стрижка",
            description="Полная стрижка",
            price_small=2500,
            price_big=3000,
        )
        serv2 = Service(
            title="Чистка",
            description="Полная Чистка",
            price_small=2500,
            price_big=3000,
        )

        appoint1 = Appointment(
            employee_id=1,
            customer_id=1,
            date=datetime.datetime.now(),
        )

        appdetail1 = AppointmentDetail(
            appointment_id=1,
            pet_id=1,
        )
        appdetail2 = AppointmentDetail(
            appointment_id=1,
            pet_id=2,
        )

        servtopet1 = ServicesToPets(
            service_id=1,
            pet_id=1,
            appointment_detail_id=1,
        )
        servtopet2 = ServicesToPets(
            service_id=2,
            pet_id=2,
            appointment_detail_id=2,
        )

        session.add(cus1)
        await session.commit()

        session.add(pet1)
        await session.commit()

        session.add(pet2)
        await session.commit()

        session.add(eml1)
        await session.commit()

        session.add(serv1)
        await session.commit()

        session.add(serv2)
        await session.commit()

        session.add(appoint1)
        await session.commit()

        session.add(appdetail1)
        await session.commit()

        session.add(appdetail2)
        await session.commit()

        session.add(servtopet1)
        await session.commit()

        session.add(servtopet2)
        await session.commit()

        my = await session.execute(
            select(Appointment)
            .filter_by(id=1)
            .options(selectinload(Appointment.details))
        )
        my = my.scalar()
        print(my)


asyncio.run(fake_db_data())
