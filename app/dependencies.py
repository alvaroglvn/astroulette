from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from app.db.db import DB

# Initialize DB instance
db_instance = DB("app/db/alien_talk.sqlite")

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_instance.engine)


# Dependency: Get session
def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session  # Provide session
    finally:
        session.close()  # Cleanup session
