from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from app.database import Base


class AppointmentDetail(Base):
    __tablename__ = "appointments_detail"
    __table_args__ = (
        UniqueConstraint("appointment_id", "pet_id", name="idx_unique_pet_appointment"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"), nullable=False
    )
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)

    def __repr__(self):
        return f"Услуги: {self.services}"
