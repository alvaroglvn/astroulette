from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import AppSettings
from app.db.db_models import User
from app.db import db_crud


DATABASE_URL = AppSettings.db_url

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


async def get_async_session() -> AsyncGenerator:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Add admin user if it hasn't been created
    async with get_async_session() as session:
        admin_user = await db_crud.get_user_by_username(session, "admin")
        if not admin_user:
            admin_user = User(username="admin", email="admin_email")
            await db_crud.create_user(session, admin_user)
