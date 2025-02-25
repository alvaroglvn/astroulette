import logging
from typing import Type, TypeVar, Optional, Any, List

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.exc import SQLAlchemyError


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


# class DB:
#     def __init__(self, filepath: str) -> None:
#         """Initialize the database engine and create tables."""
#         self.engine = create_engine(
#             f"sqlite:///{filepath}", connect_args={"check_same_thread": False}
#         )
#         self.create_tables()

#     def create_tables(self) -> None:
#         """Create all tables if they don't exist."""
#         SQLModel.metadata.create_all(self.engine)

#     def get_session(self) -> Session:
#         """Return a new session instance."""
#         return Session(self.engine)


#         # Create tables referenced by foreign keys first
#         SQLModel.metadata.create_all(
#             self.engine,
#             tables=[
#                 User.__table__,
#                 CharacterProfile.__table__,
#                 Assistant.__table__,
#                 CharacterData.__table__,
#             ],
#         )
#         # Create tables that reference them
#         SQLModel.metadata.create_all(
#             self.engine,
#             tables=[Thread.__table__, Message.__table__, UserCharacter.__table__],
#         )

#         # Load admin user
#         self.initialize_admin_user()

#     def initialize_admin_user(self) -> None:
#         with Session(self.engine) as session:
#             try:
#                 self.read_from_db(session, User, "user_name", "Admin")
#                 logging.info("Admin loaded in database")
#             except LookupError:
#                 logging.warning("No admin found. Creating new admin user...")
#                 admin_user = User(user_name="Admin", email="admin@system.local")

#                 try:
#                     self.store_entry(session, admin_user)
#                     logging.info("Admin user recorded succesfully.")
#                 except Exception as e:
#                     logging.error(f"Failed to record admin user: {e}")
#                     session.rollback()


#     # UPDATE #

#     # Generic update
#

#     # DELETE #

#     # Limited delete methods to avoid breaking databases's relationships

#     def delete_character(self, session: Session, character_id: int) -> None:
#         """Deletes a character from the database."""
#         try:
#             character = self.read_from_db(
#                 session, CharacterData, "character_id", character_id
#             )

#             session.delete(character)
#             session.commit()
#             logging.info("Character deleted.")

#         except LookupError:
#             raise ValueError(f"Character with ID {character_id} not found")

#         except Exception as e:
#             session.rollback()
#             logging.error(f"Failed to delete character: {e}")
#             raise

#     def delete_user(self, session: Session, user_id: int) -> None:
#         """Deletes a user from the database."""
#         try:
#             user = self.read_from_db(session, User, "user_id", user_id)

#             session.delete(user)
#             session.commit()
#             logging.info("User deleted.")

#         except LookupError:
#             raise ValueError(f"User with ID {user_id} not found")

#         except Exception as e:
#             session.rollback()
#             logging.error(f"Failed to delete user: {e}")
#             raise

#     # API SPECIFIC
#     def get_unmet_character(
#         self, session: Session, user_id: int
#     ) -> CharacterData | None:
#         """Returns the first character in the database the user has never seen before, or None if all have been met."""

#         try:
#             statement = (
#                 select(CharacterData)
#                 .where(
#                     CharacterData.character_id.notin_(
#                         select(UserCharacter.character_id).where(
#                             UserCharacter.user_id == user_id
#                         )
#                     )
#                 )
#                 .limit(1)
#             )

#             result = session.exec(statement).first()

#             if result:
#                 logging.info(f"Found unmet character for user {user_id}.")
#                 return result
#             else:
#                 logging.info(f"User has met all the characters in database.")
#                 return None

#         except Exception as e:
#             logging.error(
#                 f"Unable to retrieve unmet characters for user {user_id}: {e}"
#             )
#             raise
