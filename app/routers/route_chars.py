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
    background_tasks: BackgroundTasks,
) -> Response:
    # Unpack the tuple
    character_data, character_profile = character_data_profile

    # Store data in order to build db relationships
    stored_assistant = await create_record(session, assistant)
    stored_profile = await create_record(session, character_profile)

    # Set values for foreign keys relationship
    character_data.assistant_id = stored_assistant.id
    character_data.profile_id = stored_profile.id

    # Store charater data
    stored_character_data = await create_record(session, character_data)

    # Create the portrait and store its url
    if stored_character_data:

        async def add_image_url() -> None:
            if image_url := await generate_portrait(
                settings.leonardo_api_key, stored_character_data.image_prompt
            ):
                await update_record(
                    session,
                    CharacterData,
                    stored_character_data.id,
                    {"image_url": image_url},
                )

    background_tasks.add_task(add_image_url)

    return Response(status_code=201)
