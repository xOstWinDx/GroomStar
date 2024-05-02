from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import settings


class Base(DeclarativeBase):
    pass


if settings.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
    engine = create_async_engine(
        url=settings.TEST_DATABASE_URL, echo=False, **DATABASE_PARAMS
    )
else:
    engine = create_async_engine(url=settings.DATABASE_URL, echo=False)

get_async_session = async_sessionmaker(engine, expire_on_commit=False)
