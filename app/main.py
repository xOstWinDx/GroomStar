import asyncio
import datetime

from app.database import get_async_session
from app.customers.models import Customer
from app.pets.models import Pet
from app.employees.models import Employee
from app.services.models import Service
from app.appointment.models.appointment import Appointment
from app.appointment.models.appointment_detail import AppointmentDetail
from app.appointment.models.services_to_appointment import ServicesToAppointment
from sqlalchemy.orm import selectinload
from sqlalchemy import insert, select

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

        apo1 = Appointment(employee_id=1, customer_id=1, date=datetime.datetime.now())

        apodet1 = AppointmentDetail(
            appointment_id=1,
            pet_id=1,
        )
        apodet2 = AppointmentDetail(
            appointment_id=1,
            pet_id=2,
        )

        aposertodet1 = ServicesToAppointment(
            service_id=1,
            appointment_id=1,
        )

        aposertodet2 = ServicesToAppointment(
            service_id=2,
            appointment_id=1,
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
        session.add(apo1)
        await session.commit()
        session.add(apodet1)
        await session.commit()
        session.add(apodet2)
        await session.commit()
        session.add(aposertodet1)
        await session.commit()
        session.add(aposertodet2)
        await session.commit()


async def get_fake():
    async with get_async_session() as session:
        my = await session.get(Appointment, 1, options=[selectinload(Appointment.pets)])
        print(my)


# asyncio.run(fake_db_data())
asyncio.run(get_fake())
