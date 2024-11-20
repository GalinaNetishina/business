from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.config import settings

async_engine = create_async_engine(
    url=settings.asyncpg_url, echo=False, future=True, pool_size=50, max_overflow=100
)
engine = create_engine(url=settings.psycopg_url)
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
def get_session():
    ses =  sessionmaker(bind=engine)
    with ses() as session:
        yield session

async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        yield conn


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
