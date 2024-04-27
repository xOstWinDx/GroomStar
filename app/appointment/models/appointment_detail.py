from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint


from app.database import Base


if TYPE_CHECKING:
    from app.appointment.models.appointment import Appointment
    from app.services.models import Service


class AppointmentDetail(Base):
    __tablename__ = "appointments_detail"
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"), nullable=False
    )
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)

    services: Mapped[list["Service"]] = relationship(
        back_populates="appointment_detail", secondary="services_to_pets"
    )

    appointment: Mapped["Appointment"] = relationship(back_populates="details")

    def __repr__(self):
        return f"Животное #{self.pet_id} Услуги: {self.services}"
