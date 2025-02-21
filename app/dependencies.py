from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.database import get_db


# Dependency: Inject Async Database Session
def db_dependency() -> AsyncSession:
    return Depends(get_db)
