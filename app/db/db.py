from typing import TypeVar, Type

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
    def store_entry(self, data: T) -> None:

        with Session(self.engine) as session:
            try:
                print(f"Storing {data.__class__.__name__}: {data}")

                session.add(data)
                session.commit()
                session.refresh(data)
                print(f"{data.__class__.__name__} stored succesfully.")
            except Exception as e:
                print(f"Error storing {data.__class__.__name__}: {str(e)}")
                raise

    # READ #

    # Generic read
    def read_from_db(self, table: Type[T], field: str, param: str | int) -> T:
        with Session(self.engine) as session:
            print(f"Loading info from {table.__name__}")

            statement = select(table).where(getattr(table, field) == param)
            data = session.exec(statement).first()

            if data:
                return data
            else:
                raise LookupError(f"No results.")

    # Read all
    def read_all(self, table: Type[T], field: str | None = None) -> list[T]:
        """This method will return all values from a table if no field is provided, or all the values from a specific column if it is."""

        with Session(self.engine) as session:
            print(f"Loading all records from {table.__name__}")

        if field:
            statement = select(getattr(table, field))
        else:
            statement = select(table)

        results = session.exec(statement).all()

        return results if results else []

    # UPDATE #

    # Generic update
    def update_db(
        self,
        table: Type[T],
        id_field: str,
        id_value: str | int | float,
        updates: dict[str, str | int | float],
    ) -> None:
        with Session(self.engine) as session:
            print(f"Updating {table.__name__} with {updates}")

            record = self.read_from_db(table, id_field, id_value)

            for field, value in updates.items():
                if hasattr(record, field):
                    setattr(record, field, value)
                else:
                    raise LookupError(
                        f"Unable to update {field}: field does not exist    in {table.__name__}"
                    )

            session.add(record)
            session.commit()
            session.refresh(record)

            print(f"{table.__name__} update successful.")

    # DELETE #

    # Limited delete methods to avoid breaking databases's relationships

    def delete_character(self, character_id: int) -> None:
        with Session(self.engine) as session:
            character = self.read_from_db(CharacterData, "character_id", character_id)

            if character:
                session.delete(character)
                session.commit()
                print(f"Character deleted")
            else:
                raise ValueError(f"Character with id {character_id} not found.")

    def delete_user(self, user_id: int) -> None:
        with Session(self.engine) as session:
            user = self.read_from_db(User, "user_id", user_id)
            if user:
                session.delete(user)
                session.commit()
                print(f"User deleted")
            else:
                raise ValueError(f"Character with id {user_id} not found.")

    # API SPECIFIC
    def get_unmet_character(self, user_id: int) -> CharacterData | None:
        """Returns the first character in the database the user has never seen before, or None if all have been met."""

        with Session(self.engine) as session:
            statement = (
                select(CharacterData)
                .where(~CharacterData.character_id)
                .notin_(
                    select(UserCharacter.character_id).where(
                        UserCharacter.user_id == user_id
                    )
                )
            ).limit(1)

            return session.exec(statement).first()
