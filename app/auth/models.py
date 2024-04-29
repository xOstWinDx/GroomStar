import datetime
import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Jwt(Base):
    __tablename__ = "jwt"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(
        nullable=False, server_default="true", default=True
    )
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    ip_address: Mapped[str] = mapped_column(nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)
    # TODO сделать проверку браузера
