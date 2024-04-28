from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Pet(Base):
    __tablename__ = "pets"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    species: Mapped[str] = mapped_column(nullable=False)
    breed: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"#{self.id} вид: {self.species} Имя: {self.name}"
