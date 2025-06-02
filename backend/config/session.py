from typing import Annotated, AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from backend.config.settings import get_settings

app_settings = get_settings()
DATABASE_URL = app_settings.db_url

async_engine = create_async_engine(DATABASE_URL, echo=False)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=True,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for the duration of a request.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session instance.
    """
    async with get_async_session() as session:
        yield session


db_dependency = Annotated[AsyncSession, Depends(get_session)]
