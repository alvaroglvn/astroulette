from typing import TypeVar, Type

from sqlmodel import Session, create_engine, SQLModel, select

from app.db.db_models import CharacterProfile, CharacterData, User


class DB:
    # Initiate database
    def __init__(self, filepath: str) -> None:
        # Create DB Engine
        self.engine = create_engine(
            f"sqlite:///{filepath}", connect_args={"check_same_thread": False}
        )
        SQLModel.metadata.create_all(self.engine)

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

    # Generic delete limited to character or user
    def delete_entry(self, session: Session, table: Type[T], entry_id: int) -> None:

        allowed = (CharacterData, User)

        if not issubclass(table, allowed):
            raise PermissionError(f"Entries in {table.__name__} cannot be deleted.")

        entry = self.read_from_db(
            session, table, f"{table.__name__.lower()}_id", entry_id
        )

        if not entry:
            raise LookupError(f"Entry does not exist.")

        session.delete(entry)
        session.commit()
        print(f"{entry_id} deleted from {table.__name__}")
