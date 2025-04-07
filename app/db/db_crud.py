from typing import (
    Type,
    TypeVar,
    Optional,
    Any,
    List,
)
import logging
import time
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoSuchTableError
from app.models import NewCharacter
from app.db.db_models import Character, Thread, Message
from app.db.data_mappers import character_mapper
from app.db.db_excepts import TableNotFound, RecordNotFound, DatabaseError


# Global variable for type hinting
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
    session: AsyncSession, model: Type[T], primary_key: int, field: Optional[str] = None
) -> Optional[T] | Any:
    """
    Retrieve a single record or a specific field from the database.

    Args:
        session (AsyncSession): Database session
        model (Type[T]): SQLModel class to query
        primary_key (int): Primary key of the record
        field (Optional[str]): Specific field to return. If None, returns whole record

    Returns:
        Optional[Any]: The requested field value or the whole record

    Raises:
        RecordNotFound: If record doesn't exist
        TableNotFound: If table doesn't exist
        DatabaseError: For other database errors
        AttributeError: If specified field doesn't exist in model
    """
    try:
        statement = select(model).where(model.id == primary_key)
        result = await session.exec(statement)
        record = result.first()

        if not record:
            raise RecordNotFound(model.__tablename__, primary_key)

        if field:
            if not hasattr(record, field):
                raise AttributeError(f"{field} not in {model.__tablename__}")
            value = getattr(record, field)
            return value

        logging.info(f"{model} id {primary_key} found")
        return record
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__tablename__)
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("read", "Failed to read record")


async def read_all(
    session: AsyncSession, model: Type[T], **filters
) -> Optional[List[T]]:
    """Return all records from a table."""
    try:
        logging.info(f"Loading all records from {model.__tablename__}")
        statement = select(model)
        if filters:
            statement = statement.filter_by(**filters)
        result = await session.exec(statement)
        return result.all()
    except NoSuchTableError as e:
        logging.error(f"{e}")
        raise TableNotFound(model.__tablename__)
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError("read", "Failed to read records")


async def read_one_by_field(
    session: AsyncSession, model: Type[T], field_name: str, value: Any
) -> Optional[T]:
    """Read a single record based on a field other than primary key."""
    try:
        field = getattr(model, field_name)
        statement = select(model).where(field == value)
        result = await session.exec(statement)
        record = result.first()
        if not record:
            raise RecordNotFound(model.__tablename__, f"{field_name}={value}")
        return record
    except AttributeError:
        raise AttributeError(f"{field_name} is not a valid field of {model.__name__}")
    except NoSuchTableError:
        raise TableNotFound(model.__tablename__)
    except SQLAlchemyError:
        raise DatabaseError("read", f"Failed to read {model.__name__} by {field_name}")


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
) -> Optional[Character]:
    """
    Returns the first character in the database the user has never seen before,
    or None if all have been met.
    """
    try:
        statement = (
            select(Character)
            .where(
                Character.id.notin_(
                    select(Thread.character_id).where(Thread.user_id == user_id)
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
            logging.info("User has met all the characters in database.")
            return None
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError(
            "unmet characters", "Failed to retrieve unmet characters from database"
        )


async def store_new_character(
    session: AsyncSession, new_character: NewCharacter
) -> Character:
    # Map character data for storage
    character, thread = character_mapper(new_character)

    # Store character
    stored_character = await create_record(session, character)

    # Store thread data
    thread.character_id = character.id
    await create_record(session, thread)

    return stored_character


async def fetch_thread(
    session: AsyncSession,
    user_id: int,
    character_id: int,
) -> Optional[Thread]:
    try:
        statement = select(Thread).where(
            Thread.user_id == user_id, Thread.character_id == character_id
        )
        result = await session.exec(statement)
        thread = result.first()

        if thread:
            logging.info(
                f"Previous thread found between user {user_id} and character {character_id}."
            )
            return thread

        logging.info(
            f"Creating new thread between user {user_id} and character {character_id}."
        )
        new_thread = Thread(
            user_id=user_id,
            character_id=character_id,
            created_at=time.time(),
        )
        await create_record(session, new_thread)
        return new_thread
    except SQLAlchemyError as e:
        logging.error(f"{e}")
        raise DatabaseError(
            "thread", "Failed to retrieve or create thread in the database"
        )


async def store_message(
    session: AsyncSession,
    thread_id: int,
    role: str,
    content: str,
    openai_response_id: Optional[str] = None,
    created_at: int = int(time.time()),
) -> None:

    new_message = Message(
        openai_response_id=openai_response_id,
        thread_id=thread_id,
        role=role,
        content=content,
        created_at=created_at,
    )

    await create_record(session, new_message)


async def get_last_resp_id(session: AsyncSession, thread_id: int) -> Optional[str]:
    query = (
        select(Message)
        .where(Message.thread_id == thread_id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )

    result = await session.exec(query)
    last_message = result.first()

    if last_message:
        return last_message.openai_response_id
    else:
        return None
