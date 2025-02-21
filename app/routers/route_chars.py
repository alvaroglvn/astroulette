from typing import Sequence
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.dependencies import get_db
from app.db.db_models import CharacterData

router = APIRouter()


@router.get("/all-characters")
def get_characters(session: Session = Depends(get_db)) -> Sequence[CharacterData]:
    """Fetach all characters from database."""
    characters = session.exec(select(CharacterData)).all()
    return characters
