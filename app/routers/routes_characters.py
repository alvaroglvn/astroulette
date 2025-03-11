from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import *

from app.db.db_crud import *
from app.db.db_models import *
from app.db.db_excepts import *
from app.db.db_utils import *

from app.services.openai.character import new_character_parser
from app.services.openai.assistant import new_assistant_parser
from app.services.leonardo.img_request import generate_portrait


router = APIRouter()


@router.post("/generate-character")
async def new_character(
    settings: Annotated[AppSettings, Depends(settings_dependency)],
    session: db_dependency,
) -> JSONResponse:
    try:
        async with session.begin():
            # Generate character data and profile
            character_data, character_profile = new_character_parser(
                settings.openai_api_key
            )

            # Generate assistant
            assistant = new_assistant_parser(settings.openai_api_key, character_profile)

            # DB storage
            # 1. Store assistant and build relationshop with character data
            stored_assistant = await create_record(session, assistant)
            character_data.assistant_id = stored_assistant.id
            # 2. Store character profile adn build relationship with character data
            stored_profile = await create_record(session, character_profile)
            character_data.profile_id = stored_profile.id
            # 4. Build user relationship with character data
            character_data.generated_by = (
                1  # Admin user until user system is      implemented
            )
            # 5. Generate character portrait
            prompt = character_data.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            if portrait_url:
                character_data.image_url = portrait_url
            else:
                raise Exception("Failed to generate character portrait")

            # 6. Store character data
            stored_character_data = await create_record(session, character_data)

            return JSONResponse(
                content={
                    "profile": stored_profile.model_dump(),
                    "character": stored_character_data.model_dump(),
                },
                status_code=201,
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
        )
