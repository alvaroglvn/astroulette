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
                self.read_from_db(session, User, "user_name", "Admin")
                print("Admin loaded in database")
            except LookupError:
                print("No admin found. Creatind new admin user...")

                admin_user = User(user_name="Admin", email="admin@system.local")
                self.store_entry(session, admin_user)

                print("Admin user created succesfully.")

    # Define generic type
    T = TypeVar("T", bound=SQLModel)

    # CREATE #

    # Generic storage
    def store_entry(self, session: Session, data: T) -> None:

        try:
            print(f"Storing {data.__class__.__name__}:     {data}")

            session.add(data)
            session.commit()
            session.refresh(data)
            print(f"{data.__class__.__name__} stored   succesfully.")
        except Exception as e:
            print(f"Error storing {data.__class__.__name__}: {str(e)}")
            raise

    # READ #

    # Generic read
    def read_from_db(
        self, session: Session, table: Type[T], field: str, param: str | int
    ) -> T:
        print(f"Loading info from {table.__name__}")

        statement = select(table).where(getattr(table, field) == param)
        data = session.exec(statement).first()

        if data:
            return data
        else:
            raise LookupError(f"No results.")

    # UPDATE #

    # Generic update
    def update_db(
        self,
        session: Session,
        table: Type[T],
        id_field: str,
        id_value: str | int | float,
        updates: dict[str, str | int | float],
    ) -> None:
        print(f"Updating {table.__name__} with {updates}")

        record = self.read_from_db(session, table, id_field, id_value)

        for field, value in updates.items():
            if hasattr(record, field):
                setattr(record, field, value)
            else:
                raise LookupError(
                    f"Unable to update {field}: field does not exist in {table.__name__}"
                )

        session.add(record)
        session.commit()
        session.refresh(record)

        print(f"{table.__name__} update successful.")

    # DELETE #

    # Limited delete methods to avoid breaking databases's relationships

    def delete_character(self, session: Session, character_id: int) -> None:
        character = self.read_from_db(
            session, CharacterData, "character_id", character_id
        )

        if character:
            session.delete(character)
            session.commit()
            print(f"Character deleted")
        else:
            raise ValueError(f"Character with id {character_id} not found.")

    def delete_user(self, session: Session, user_id: int) -> None:
        user = self.read_from_db(session, User, "user_id", user_id)
        if user:
            session.delete(user)
            session.commit()
            print(f"User deleted")
        else:
            raise ValueError(f"Character with id {user_id} not found.")
