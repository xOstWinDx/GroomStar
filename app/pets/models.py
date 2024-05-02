from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship


from app.database import Base
from app.users.models import User


class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    species: Mapped[str] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="pets")

    def __repr__(self):
        return f"#{self.id} {self.species} Кличка: {self.name}"
