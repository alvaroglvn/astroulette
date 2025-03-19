from typing import AsyncGenerator
import logging
from contextlib import asynccontextmanager

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import AppSettings
from app.db.db_models import User
from app.db.db_crud import create_record, read_record, RecordNotFound


app_settings = AppSettings()
DATABASE_URL = app_settings.db_url

async_engine = create_async_engine(DATABASE_URL, echo=False)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database and load admin user."""
    try:
        # [Emergency drop all in case db schema doesn't update]
        # async with async_engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.drop_all)

        # Create all tables
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            logging.info("Database tables created successfully")

        # Load admin user
        success = await load_admin()
        if not success:
            logging.error("Failed to load admin user")

    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise


async def load_admin() -> bool:
    """
    Load or create admin user in database.
    Returns True if successful, False otherwise.
    """
    try:
        async with get_async_session() as session:
            try:
                admin = await read_record(session, User, 1)
            except RecordNotFound:
                logging.info("Admin user not found, creating new admin user")
                admin = User(
                    username="admin",
                    email="admin@admin.com",
                    active=True,
                )
                await create_record(session, admin)
                logging.info("Admin user created successfully")
                return True

            logging.info("Admin user already exists")
            return True

    except Exception as e:
        logging.error(f"Error loading admin user: {e}")
        return False
