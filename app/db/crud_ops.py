from typing import TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import Base


T = TypeVar("T", bound=Base)

# CREATE


async def create_entry(session: AsyncSession, model: Type[T], entry: T) -> bool:
    """Stores new entry in the database"""
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return True


# READ


async def read_entry(session: AsyncSession, model: Type[T], entry_id: int) -> T:
    """Retrieve a single entry by id from anywhere in the database."""
    result = await session.execute(select(model).where(model.id == entry_id))
    return result.scalar_one_or_none()


async def read_all(session: AsyncSession, model: Type[T]) -> List[T]:
    """Retrieved all entries from a specific model"""
    result = await session.execute(select(model))
    return result.scalars().all()
