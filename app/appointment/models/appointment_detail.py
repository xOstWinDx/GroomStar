from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base
from app.services.models import Service
from app.pets.models import Pet

if TYPE_CHECKING:
    from app.appointment.models.appointment import Appointment


class AppointmentDetail(Base):
    __tablename__ = "appointments_detail"
    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey("appointments.id"), nullable=False
    )
    pet_id: Mapped[int] = mapped_column(ForeignKey("pets.id"), nullable=False)

    services: Mapped[list["Service"]] = relationship(
        secondary="services_to_pets", lazy="selectin"
    )
    pet: Mapped["Pet"] = relationship(lazy="selectin")

    appointment: Mapped["Appointment"] = relationship(
        back_populates="details", lazy="selectin"
    )

    def __repr__(self):
        return f"Животное {self.pet} Услуги: {self.services}"
