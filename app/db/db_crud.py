import logging
from typing import Type, TypeVar, Optional, Any, List

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.exc import SQLAlchemyError

from app.db.db_models import CharacterData, UserCharacters


T = TypeVar("T", bound=SQLModel)


# CREATE
async def create_record(session: AsyncSession, record: T) -> Optional[T]:
    """Store a new entry of any kind to the database.

    Args:
        session (AsyncSession): The database session.
        record (T): The record to be created.

    Returns:
        Optional[T]: The created record or None if creation failed.
    """
    try:
        logging.info(f"Creating new record {record.__class__.__name__}")
        session.add(record)
        await session.commit()
        await session.refresh(record)
        logging.info(f"New record {record.__class__.__name__} created successfully")
        return record
    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Error creating new record {record.__class__.__name__}: {e}")
        return None


# READ
async def read_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
) -> Optional[T]:
    """Retrieve a single record from the database.

    Args:
        session (AsyncSession): The database session.
        model (Type[T]): The table to read.

    Returns:
        Optional[T]: The found record or None.

    """

    # Catch error if the table doesn't exist
    if model.__tablename__ not in SQLModel.metadata.tables:
        raise ValueError(f"Table {model.__tablename__} does not exist.")

    try:
        primary_key_column = list(model.__table__.primary_key)[0]
        statement = select(model).where(primary_key_column == primary_key)
        result = await session.exec(statement)

        return result.one_or_none()
    except SQLAlchemyError as e:
        logging.error(f"Unable to read from table {model.__tablename__}: {e}")
        raise


async def read_all(session: AsyncSession, model: Type[T]) -> List[T]:
    """Return all records from a table.

    Args:
        session (AsyncSession): The database session.
        model (Type[T]): The table to read.

    Returns:
        List[T]: A list of records from the table.
    """

    if model.__tablename__ not in SQLModel.metadata.tables:
        raise ValueError(f"Table {model.__tablename__} does not exist")

    try:
        logging.info(f"Loading all records from {model.__tablename__}")

        statement = select(model)
        result = await session.exec(statement)
        results = result.all()

        if not results:
            logging.info(f"No results found.")

        return results

    except SQLAlchemyError as e:
        logging.error(f"Unable to read from table {model.__tablename__}: {e}")
        raise


# UPDATE
async def update_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
    updates: dict[str, Any],
) -> Optional[T]:
    """Update an existing record in the database.

    Args:
        session (AsyncSession): The database session.
        model (Type[T]): The table to update.
        primary_key (int): The primary key of the record to update.
        updates (dict[str, Any]): A dictionary of fields and values to update.

    Returns:
        Optional[T]: The updated record or None if update failed.
    """
    if model.__tablename__ not in SQLModel.metadata.tables:
        raise ValueError(f"Table {model.__tablename__} does not exist")

    try:
        primary_key_column = list(model.__table__.primary_key)[0]
        statement = select(model).where(primary_key_column == primary_key)
        result = await session.exec(statement)
        record = result.one_or_none()

        if not record:
            logging.warning(
                f"Record with primary key {primary_key} not found in {model.__tablename__}"
            )
            return None

        for field, value in updates.items():
            if hasattr(record, field):
                setattr(record, field, value)

        await session.commit()
        await session.refresh(record)
        logging.info(
            f"Record {model.__tablename__} with primary key {primary_key} updated successfully"
        )
        return record

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Unable to update table {model.__tablename__}: {e}")
        return None


# DELETE
async def delete_record(
    session: AsyncSession,
    model: Type[T],
    primary_key: int,
) -> bool:
    """Delete a record from the database.

    Args:
        session (AsyncSession): The database session.
        model (Type[T]): The table to delete from.
        primary_key (int): The primary key of the record to delete.

    Returns:
        bool: True if the record was deleted successfully, False otherwise.
    """
    if model.__tablename__ not in SQLModel.metadata.tables:
        raise ValueError(f"Table {model.__tablename__} does not exist")

    try:
        primary_key_column = list(model.__table__.primary_key)[0]
        statement = select(model).where(primary_key_column == primary_key)
        result = await session.exec(statement)
        record = result.one_or_none()

        if not record:
            logging.warning(
                f"Record with primary key {primary_key} not found in {model.__tablename__}"
            )
            return False

        await session.delete(record)
        await session.commit()
        logging.info(
            f"Record {model.__tablename__} with primary key {primary_key} deleted successfully"
        )
        return True

    except SQLAlchemyError as e:
        await session.rollback()
        logging.error(f"Unable to delete from table {model.__tablename__}: {e}")
        return False


# API SPECIFIC


async def fetch_unmet_character(
    session: AsyncSession, user_id: int
) -> Optional[CharacterData]:
    """
    Returns the first character in the database the user has never seen before,
    or None if all have been met.

    Args:
        session (AsyncSession): The database session.
        user_id (int): The ID of the user.

    Returns:
        Optional[CharacterData]: The first unmet character or None if all have been met.
    """

    try:
        statement = (
            select(CharacterData)
            .where(
                CharacterData.character_id.notin_(
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
        logging.error(f"Unable to retrieve unmet characters for user {user_id}: {e}")
        raise
