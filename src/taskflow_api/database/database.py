# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from taskflow_api.config.settings import settings
# DATABASE_URL ="sqlite:///./taskflow.db"


# engine = create_engine(
#     DATABASE_URL,
#     echo=True
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False
# )

# class Base(DeclarativeBase):
#     pass



DATABASE_URL = "sqlite+aiosqlite:///./taskflow.db"

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass