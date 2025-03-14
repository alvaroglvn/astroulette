from typing import Type, TypeVar, Optional, Any, List
import logging
import time

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.exc import SQLAlchemyError, NoSuchTableError

from app.db.db_models import CharacterData, UserCharacters, Thread
from app.db.db_excepts import *


T = TypeVar("T", bound=SQLModel)


# CREATE
async def create_record(session: AsyncSession, record: T) -> Optional[T]:
    """Store a new entry of any kind to the database."""
    try:
        logging.info(f"Creating new record {record.__class__.__name__}")
        session.add(record)
        await session.commit()
        await session.refresh(record)
        logging.info(f"New record {record.__class__.__name__} created successfully")
        return record
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(record.__tablename__)
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("create", "Failed to store new record")


# READ
async def read_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
) -> Optional[T]:
    """Retrieve a single record from the database."""
    try:
        statement = select(model).where(model.id == primary_key)
        result = await session.exec(statement)
        record = result.first()
        if not record:
            raise RecordNotFound(model.__tablename__, primary_key)
        logging.info(f"{model} id {primary_key} found")
        return record
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__tablename__)
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("read", "Failed to read record")


async def read_all(session: AsyncSession, model: Type[T]) -> Optional[List[T]]:
    """Return all records from a table."""
    try:
        logging.info(f"Loading all records from {model.__tablename__}")
        statement = select(model)
        result = await session.exec(statement)
        return result.all()
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__tablename__)
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("read", "Failed to read records")


# UPDATE
async def update_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
    updates: dict[str, Any],
) -> Optional[T]:
    """Update an existing record in the database."""
    try:
        record = await read_record(session, model, primary_key)
        for field, value in updates.items():
            if hasattr(record, field):
                setattr(record, field, value)
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__tablename__)
    except RecordNotFound:
        raise
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("update", "Failed to update record")


# DELETE
async def delete_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
) -> None:
    """Delete a record from the database."""
    try:
        record = await read_record(session, model, primary_key)
        await session.delete(record)
        await session.commit()
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__name__)
    except RecordNotFound:
        raise
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("delete", "Failed to delete record")


# API SPECIFIC


async def fetch_unmet_character(
    session: AsyncSession, user_id: int
) -> Optional[CharacterData]:
    """
    Returns the first character in the database the user has never seen before,
    or None if all have been met.
    """
    try:
        statement = (
            select(CharacterData)
            .where(
                CharacterData.id.notin_(
                    select(UserCharacters.character_id).where(
                        UserCharacters.user_id == user_id
                    )
                )
            )
            .limit(1)
        )
        result = await session.exec(statement)
        character = result.first()
        if character:
            logging.info(f"Found unmet character for user {user_id}.")
            return character
        else:
            logging.info(f"User has met all the characters in database.")
            return None
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError(
            "unmet characters", "Failed to retrieve unmet characters from database"
        )


async def fetch_thread(
    session: AsyncSession,
    user_id: int,
    character_id: int,
) -> Optional[Thread]:
    try:
        thread = read_record(session, Thread, Thread.id).where(
            Thread.user_id == user_id, Thread.character_id == character_id
        )
        if thread:
            logging.info(
                f"Previous thread found between user {user_id} and character {character_id}."
            )
            return thread
        else:
            logging.info(
                f"Creating new thread between user {user_id} and character {character_id}."
            )
            new_thread = Thread(
                user_id=user_id,
                character_id=character_id,
                created_at=time.time(),
            )
            return new_thread
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("thread", "Failed to retrieve thread from database")
