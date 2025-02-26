from typing import Annotated
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session

from app.dependencies import *
from app.services.openai.character_gen import generate_character
from app.services.openai.assistant_gen import generate_assistant
from app.db.db_crud import *

router = APIRouter()


@router.get("/new-character")
async def new_character(
    settings: Annotated[AppSettings, Depends(settings_dependency)],
    session: Annotated[Session, Depends(db_dependency)],
) -> Response:
    """Generates a new character and stores it in the database"""

    try:

        # 1. Generate CharacterData and CharacterProfile
        character_data, character_profile = generate_character(settings.openai_api_key)

        # 2. Generate Assistant
        assistant = generate_assistant(settings.openai_api_key, character_data)

        # 3. Save to database in order
        await create_record(assistant)
        await create_record(character_profile)
        await create_record(character_data)

        return Response(content="New character created.", status_code=201)

    except Exception as e:
        session.rollback()
        return Response(
            content=f"Failed to create new character: {e}.", status_code=500
        )
