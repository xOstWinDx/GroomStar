from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.appointment.models.appointment import Appointment


class Employee(Base):
    __tablename__ = "employees"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    appointments: Mapped[list["Appointment"]] = relationship(back_populates="employee")

    def __repr__(self):
        return f"#{self.id} {self.full_name} {self.email}"
