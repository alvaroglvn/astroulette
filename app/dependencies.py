from typing import Generator
from sqlmodel import Session
from app.db.db import DB

# Initialize DB instance
db_instance = DB("app/db/alien_talk.sqlite")


# Dependency: Get session
def get_db() -> Generator[Session, None, None]:
    session = db_instance.get_session()
    try:
        yield session
    finally:
        session.close()
