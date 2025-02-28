from typing import Annotated
from fastapi import APIRouter, Depends, Response, BackgroundTasks
from sqlmodel import Session

from app.dependencies import *

from app.db.db_crud import *
from app.db.db_models import *
from app.db.db_excepts import *

from app.services.openai.character import generate_character
from app.services.openai.assistant import generate_assistant, create_db_assistant
from app.services.leonardo.img_request import generate_portrait


router = APIRouter()


@router.get("/new-character")
async def new_character(
    settings: Annotated[AppSettings, Depends(settings_dependency)],
    session: Annotated[Session, Depends(db_dependency)],
    background_tasks: BackgroundTasks,
) -> Response:
    try:
        character_data, character_profile = generate_character(settings.openai_api_key)
        assistant = generate_assistant(settings.openai_api_key, character_data)
        db_assistant = create_db_assistant(assistant)

        # stored_assistant = await create_record(session, db_assistant)
        stored_profile = await create_record(session, character_profile)

        # character_data.assistant_id = stored_assistant.id
        character_data.profile_id = stored_profile.id

        stored_character_data = create_record(session, character_data)

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

        return Response(content="New character created", status_code=201)

    except (DatabaseError, RecordNotFound, TableNotFound) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error"
        )
