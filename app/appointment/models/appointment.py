import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.appointment.models.appointment_detail import AppointmentDetail


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )

    details: Mapped[list["AppointmentDetail"]] = relationship(
        back_populates="appointment", lazy="selectin"
    )

    def __repr__(self):
        return f"Запись #{self.id} Работник: #{self.employee_id}, Клиент: #{self.id}. детали: {self.details}"
