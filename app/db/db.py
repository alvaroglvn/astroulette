from typing import TypeVar, Type
import logging

from sqlmodel import Session, create_engine, SQLModel, select

from app.db.db_models import *


class DB:
    # Initiate database
    def __init__(self, filepath: str) -> None:
        # Create DB Engine
        self.engine = create_engine(
            f"sqlite:///{filepath}", connect_args={"check_same_thread": False}
        )
        # Create tables referenced by foreign keys first
        SQLModel.metadata.create_all(
            self.engine,
            tables=[
                User.__table__,
                CharacterProfile.__table__,
                Assistant.__table__,
                CharacterData.__table__,
            ],
        )
        # Create tables that reference them
        SQLModel.metadata.create_all(
            self.engine,
            tables=[Thread.__table__, Message.__table__, UserCharacter.__table__],
        )

        # Load admin user
        self.initialize_admin_user()

    def initialize_admin_user(self) -> None:
        with Session(self.engine) as session:
            try:
                self.read_from_db(User, "user_name", "Admin")
                print("Admin loaded in database")
            except LookupError:
                print("No admin found. Creatind new admin user...")

                admin_user = User(user_name="Admin", email="admin@system.local")
                self.store_entry(admin_user)

                print("Admin user created succesfully.")

    def get_session(self) -> Session:
        return Session(self.engine)

    # Define generic type
    T = TypeVar("T", bound=SQLModel)

    # CREATE #

    # Generic storage
    def store_entry(self, session: Session, data: T) -> None:
        """Store a new entry of any kind to the database."""
        try:
            logging.info(f"Storing {data.__class__.__name__}:{data}")
            session.add(data)
            session.commit()
            session.refresh(data)
            logging.info(f"{data.__class__.__name__} stored succesfully.")
        except Exception as e:
            logging.error(f"Error storing {data.__class__.__name__}: {str(e)}")
            raise

    # READ #

    # Generic read
    def read_from_db(
        self, session: Session, table: Type[T], field: str, value: str | int
    ) -> T:
        """Fetch a single record from the database based on a specific field and value."""

        if table.__tablename__ not in SQLModel.metadata.tables:
            raise ValueError(f"Table {table.__tablename__} does not exist")

        if not hasattr(table, field):
            raise ValueError(f"Field {field} does not exist in {table.__tablename__}")

        logging.info(f"Searching for value in {table.__tablename__}: {field} = {value}")

        statement = select(table).where(getattr(table, field) == value)
        result = session.exec(statement).first()

        if not result:
            raise LookupError(f"No record found.")

        logging.info("Record found.")
        return result

    # Read all
    def read_all(
        self, table: Type[T], session: Session, field: str | None = None
    ) -> list[T]:
        """Return all values from a table if no column is provided, or all the values from a specific column if it is."""

        if table.__tablename__ not in SQLModel.metadata.tables:
            raise ValueError(f"Table {table.__tablename__} does not exist")

        logging.info(f"Loading all records from {table.__tablename__}")

        if field:
            if not hasattr(table, field):
                raise ValueError(f"Field does not exist in {table.__tablename__}")
            statement = select(getattr(table, field))
        else:
            statement.select(table)

        results = session.exec(statement).all()

        if not results:
            raise LookupError(f"No records found in {table.__tablename__}")

        return results

    # UPDATE #

    # Generic update
    def update_db(
        self,
        table: Type[T],
        session: Session,
        id_field: str,
        id_value: str | int | float,
        updates: dict[str, str | int | float],
    ) -> None:
        """Updates an existing record in the database."""

        if table.__tablename__ not in SQLModel.metadata.tables:
            raise ValueError(f"Table {table.__tablename__} does not exist")

        logging.info(f"Updating {table.__tablename__} with {updates}")

        record = self.read_from_db(session, table, id_field, id_value)

        for field, value in updates.items():
            if hasattr(record, field):
                setattr(record, field, value)
            else:
                raise ValueError(
                    f"Unable to update {field}: field does not exist in{table.__tablename__}"
                )
        try:
            session.add(record)
            session.commit()
            session.refresh(record)
            logging.info(f"{table.__tablename__} updated successfully.")
        except Exception as e:
            session.rollback()
            logging.error(f"Failed to update {table.__tablename__}: {e}")
            raise

    # DELETE #

    # Limited delete methods to avoid breaking databases's relationships

    def delete_character(self, session: Session, character_id: int) -> None:
        """Deletes a character from the database."""
        try:
            character = self.read_from_db(
                session, CharacterData, "character_id", character_id
            )

            session.delete(character)
            session.commit()
            logging.info("Character deleted.")

        except LookupError:
            raise ValueError(f"Character with ID {character_id} not found")

        except Exception as e:
            session.rollback()
            logging.error(f"Failed to delete character: {e}")
            raise

    def delete_user(self, session: Session, user_id: int) -> None:
        """Deletes a user from the database."""
        try:
            user = self.read_from_db(session, User, "user_id", user_id)

            session.delete(user)
            session.commit()
            logging.info("User deleted.")

        except LookupError:
            raise ValueError(f"User with ID {user_id} not found")

        except Exception as e:
            session.rollback()
            logging.error(f"Failed to delete user: {e}")
            raise

    # API SPECIFIC
    def get_unmet_character(
        self, session: Session, user_id: int
    ) -> CharacterData | None:
        """Returns the first character in the database the user has never seen before, or None if all have been met."""

        try:
            statement = (
                select(CharacterData)
                .where(CharacterData.character_id)
                .notin_(
                    select(UserCharacter.character_id).where(
                        UserCharacter.user_id == user_id
                    )
                )
            ).limit(1)

            result = session.exec(statement).first()

            if result:
                logging.info(f"Found unmet character for user {user_id}.")
                return result
            else:
                logging.info(f"User has met all the characters in database.")
                return None

        except Exception as e:
            logging.error(
                f"Unable to retrieve unmet characters for user {user_id}: {e}"
            )
            raise
