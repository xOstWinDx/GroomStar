import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime


from app.database import Base


if TYPE_CHECKING:
    from app.appointment.models.appointment import Appointment
    from app.pets.models import Pet


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    is_employee: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default="false",
        index=True,
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default="false",
        nullable=False,
    )
    registration_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        default=datetime.datetime.now(),
    )

    pets: Mapped[list["Pet"]] = relationship(back_populates="user", lazy="selectin")
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="customer", foreign_keys="appointments.c.customer_id"
    )

    def __repr__(self):
        return f"#{self.id} {self.full_name} {self.phone} {self.email}"
