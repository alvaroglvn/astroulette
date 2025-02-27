from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_setup import get_async_session
from app.db.db_models import *
from app.config import AppSettings
from app.services.openai.character_gen import generate_character
from app.services.openai.assistant_gen import generate_assistant
from app.services.leonardo.img_request import generate_portrait


def db_dependency() -> AsyncSession:
    """
    Dependency function that provides an asynchronous database session.

    This function uses the FastAPI `Depends` utility to inject an instance of
    `AsyncSession` from the `get_async_session` function. It is typically used
    as a dependency in route handlers to interact with the database.

    Returns:
        AsyncSession: An instance of the asynchronous database session.
    """
    return Depends(get_async_session)


def settings_dependency() -> AppSettings:
    """
    Provides an instance of the AppSettings class.

    This function serves as a dependency provider for the application settings,
    ensuring that an instance of AppSettings is available wherever it is needed.

    Returns:
        AppSettings: An instance of the AppSettings class.
    """
    return AppSettings()


async def generate_character_dependency(
    settings: Annotated[AppSettings, Depends(settings_dependency)]
) -> tuple[CharacterData, CharacterProfile]:
    return await generate_character(settings.openai_api_key)


async def generate_assistant_dependency(
    settings: Annotated[AppSettings, Depends(settings_dependency)],
    character_data: Annotated[CharacterData, Depends(generate_character_dependency)],
) -> Assistant:
    return await generate_assistant(settings.openai_api_key, character_data)
