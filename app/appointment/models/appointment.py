import datetime
from typing import TYPE_CHECKING
from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.appointment.models.appointment_detail import AppointmentDetail

if TYPE_CHECKING:
    from app.pets.models import Pet
    from app.services.models import Service


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )

    pets: Mapped[list["Pet"]] = relationship(
        back_populates="appointments",
        secondary="appointments_detail",
        lazy="selectin",
    )

    services: Mapped[list["Service"]] = relationship(
        back_populates="appointment",
        secondary="services_to_appointment",
        lazy="selectin",
    )

    def __repr__(self):
        return f"Запись #{self.id} Работник: {self.employee_id}, Клиент: {self.id}. Животные: {self.pets} Услуги: {self.services}"
