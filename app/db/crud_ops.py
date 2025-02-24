from typing import TypeVar, Type, List, Optional, Any
import logging
from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import Base


T = TypeVar("T", bound=Base)


# CREATE
async def create_record(session: AsyncSession, record: T) -> Optional[T]:
    """Stores new record in the database"""
    try:
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Failed to add record to database: {str(e)}")
        raise


# READ
async def read_record(
    session: AsyncSession, model: Type[T], primary_key: int
) -> Optional[T]:
    """Retrieve a single record by id from anywhere in the database."""
    try:
        result = await session.execute(select(model).where(model.id == primary_key))
        value = result.scalar_one_or_none()

        if value is None:
            logging.warning(f"No value found in {model.__name__} with ID {primary_key}")

        return value

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Failed to retrieve value from {model}: {e}")
        raise


async def read_all(
    session: AsyncSession, model: Type[T], order_by: Any = None
) -> Optional[List[T]]:
    """Retrieve all entries from a specific model, ordered or not."""
    try:
        query = select(model)
        if order_by:
            query = query.order_by(order_by)

        result = await session.execute(query)
        entries = result.scalars().all()

        if not entries:
            logging.warning(f"No values found in {model.__name__}")

        return entries

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Unable to read values from {model.__name__}: {e}")
        raise


# UPDATE
async def update_record(
    session: AsyncSession, record: T, update_fields: dict
) -> Optional[T]:
    """Update an exisiting field with new values."""
    if not record:
        logging.error("Cannot update an record that doesn't exist.")
        raise DatabaseError

    # Check if the fields to update are valid
    valid_fields = {column.name for column in record.__table__.columns}
    invalid_fields = [key for key in update_fields if key not in valid_fields]

    if invalid_fields:
        raise ValueError(f"Invalid field/s: {invalid_fields}.")

    try:
        for key, value in update_fields.items():
            if hasattr(record, key):
                setattr(record, key, value)

        await session.commit()
        await session.refresh(record)
        return record
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Failed to update {record.__class__.__name__}: {e}")
        raise


# DELETE
async def delete_record(session: AsyncSession, record: T) -> bool:
    """Safely delete an record from the database"""
    if not record:
        raise ValueError("Cannot delete an record that doesn't exist.")

    try:
        await session.delete(record)
        await session.commit()
        return True

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Failed to delete {record.__class__.__name__}: {e}")
        raise
