from fastapi import APIRouter, BackgroundTasks, Response, Depends
from sqlalchemy.orm import Session
from app.services.openai.character_gen import character_generator
from app.utils.data_validator import validate_data
from app.dependencies import get_db
from app.db.db_models import CharacterData, CharacterProfile
from app.config import AppSettings


router = APIRouter()


@router.get("/new-character")
def create_new(
    config: AppSettings, session: Session = Depends(get_db), db_instance: DB = Depends()
) -> Response:
    # 1. Generate and store new character
    new_character = character_generator(config.openai_api_key)

    if not new_character:
        return Response(
            content="Unable to fetch new character from OpenAI.", status_code=500
        )

    # Validate character profile
    valid_profile = validate_data(new_character["character_profile"], CharacterProfile)
    if not valid_profile:
        return Response(
            content="Unable to validate character profile.", status_code=500
        )
    # Validate character data
    valid_character_data = validate_data(CharacterData, new_character)
    if not valid_character_data:
        return Response(content="Unable to validate character data.", status_code=500)

    # 2. Store new character
    db.store_entry(db, valid_character_data)

    pass
