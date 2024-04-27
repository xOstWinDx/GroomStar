from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.appointment.models.appointment import Appointment


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price_small: Mapped[int] = mapped_column(nullable=False)
    price_big: Mapped[int] = mapped_column(nullable=False)

    appointment: Mapped[list["Appointment"]] = relationship(
        back_populates="services",
        secondary="services_to_appointment",
    )

    def __repr__(self):
        return f"#{self.id} {self.title}"
