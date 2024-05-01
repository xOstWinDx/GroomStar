import datetime

from sqlalchemy import insert, select, func

from app.appointment.models.appointment import Appointment
from app.appointment.models.appointment_detail import AppointmentDetail
from app.appointment.models.services_to_pets import ServicesToPets
from app.dao.base import BaseDAO
from app.database import get_async_session


class AppointmentDAO(BaseDAO):
    model = Appointment

    @classmethod
    async def add(
        cls,
        employee_id,
        customer_id,
        date,
        details,
    ):
        async with get_async_session() as session:
            apo_id = await session.execute(
                insert(Appointment)
                .values(
                    employee_id=employee_id,
                    customer_id=customer_id,
                    date=date,
                )
                .returning(Appointment.id)
            )
            apo_id = apo_id.scalar()

            for detail in details:
                pet_id = detail["pet_id"]
                detail_id = await session.execute(
                    insert(AppointmentDetail)
                    .values(
                        appointment_id=apo_id,
                        pet_id=pet_id,
                    )
                    .returning(AppointmentDetail.id)
                )
                detail_id = detail_id.scalar()
                for service_id in detail["services"]:
                    await session.execute(
                        insert(ServicesToPets).values(
                            service_id=service_id,
                            appointment_detail_id=detail_id,
                        )
                    )
            await session.commit()

    @classmethod
    async def get_date_of_employees(cls, date: datetime.datetime, employee_id):
        async with get_async_session() as session:
            res = await session.execute(
                select(cls.model.date)
                .where(func.DATE(cls.model.date) == date.date())
                .filter_by(employee_id=employee_id)
            )
            res = res.scalars().all()
            return res
