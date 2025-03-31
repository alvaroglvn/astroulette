from typing import AsyncGenerator, Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_setup import get_async_session
from app.db.db_models import *
from app.config import AppSettings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session() as session:
        try:
            yield session
        finally:
            await session.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


def get_settings() -> AppSettings:
    """
    Provides an instance of the AppSettings class.

    This function serves as a dependency provider for the application settings,
    ensuring that an instance of AppSettings is available wherever it is needed.

    Returns:
        AppSettings: An instance of the AppSettings class.
    """
    return AppSettings()


settings_dependency = Annotated[AppSettings, Depends(get_settings)]
