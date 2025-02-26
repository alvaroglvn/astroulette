from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import AppSettings

app_settings = AppSettings()
DATABASE_URL = app_settings.db_url

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def init_db() -> None:
    # First create all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
