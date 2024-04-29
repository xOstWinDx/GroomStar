import uuid

from sqlalchemy import update

from app.auth.models import Jwt
from app.dao.base import BaseDAO
from app.database import get_async_session


class JwtDAO(BaseDAO):
    model = Jwt

    @classmethod
    async def update(cls, token_id: uuid.UUID, is_active: bool) -> model:
        async with get_async_session() as session:
            result = await session.execute(
                update(cls.model).values(is_active=is_active).filter_by(id=token_id)
            )
            result = result.rowcount
            await session.commit()
        return result
