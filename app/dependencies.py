from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.db_setup import get_async_session
from app.config import AppSettings


# Dependency: Inject Async Database Session
def db_dependency() -> AsyncSession:
    return Depends(get_async_session)


# Dependency: Inject AppSettings
def settings_dependency() -> AppSettings:
    return AppSettings()
