from typing import Annotated
from fastapi import APIRouter, Depends, Response, BackgroundTasks
from sqlmodel import Session

from app.dependencies import *

from app.db.db_crud import *
from app.db.db_models import *


router = APIRouter()


@router.get("/new-character")
async def new_character(
    settings: Annotated[AppSettings, Depends(settings_dependency)],
    session: Annotated[Session, Depends(db_dependency)],
    character_data_profile: Annotated[
        tuple[CharacterData, CharacterProfile], Depends(generate_character_dependency)
    ],
    assistant: Annotated[Assistant, Depends(generate_assistant_dependency)],
) -> Response:
    # Unpack the tuple
    character_data, character_profile = character_data_profile

    # Store data in order to build db relationships
    stored_assistant = await create_record(session, assistant)
    stored_profile = await create_record(session, character_profile)

    # Set values for foreign keys relationship
    character_data.assistant_id = stored_assistant.id
    character_data.profile_id = stored_profile.id

    create_record(session, character_data)

    return Response(status_code=201)
