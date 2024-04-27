from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class ServicesToPets(Base):
    __tablename__ = "services_to_pets"
    __table_args__ = (
        UniqueConstraint(
            "service_id",
            "appointment_detail_id",
            name="idx_unique_service_id_detail_id",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    appointment_detail_id: Mapped[int] = mapped_column(
        ForeignKey("appointments_detail.id"), nullable=False
    )
