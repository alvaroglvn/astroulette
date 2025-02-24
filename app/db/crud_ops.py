from typing import TypeVar, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import Base


T = TypeVar("T", bound=Base)


# CREATE
async def create_entry(session: AsyncSession, entry: T) -> T:
    """Stores new entry in the database"""
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


# READ
async def read_by_id(
    session: AsyncSession, model: Type[T], entry_id: int
) -> Optional[T]:
    """Retrieve a single entry by id from anywhere in the database."""
    result = await session.execute(select(model).where(model.id == entry_id))
    return result.scalar_one_or_none()


async def read_all(
    session: AsyncSession, model: Type[T], order_by: Any = None
) -> List[T]:
    """Retrieve all entries from a specific model, ordered or not."""
    query = select(model)
    if order_by:
        query = query.order_by(order_by)

    result = await session.execute(query)
    return result.scalars().all()


# UPDATE
async def update_entry(session: AsyncSession, entry: T, updates: dict) -> bool:
    """Update an exisiting field with new values."""
    for key, value in updates.items():
        if hasattr(entry, key):
            setattr(entry, key, value)

    await session.commit()
    await session.refresh(entry)
    return True


# DELETE
async def delete_entry(session: AsyncSession, entry: T) -> bool:
    """Delete an entry from the database"""
    if not entry:
        return False
    await session.delete(entry)
    await session.commit()
    return True
