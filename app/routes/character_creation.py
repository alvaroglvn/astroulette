from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import *

from app.db.db_crud import *
from app.db.db_models import *
from app.db.db_excepts import *
from app.db.db_utils import *

from app.services.openai.character import new_character_parser
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
            character_data, character_profile, thread = new_character_parser(
                settings.openai_api_key
            )

            # DB storage
            # 1. Store character profile adn build relationship with character data
            stored_profile = await create_record(session, character_profile)
            character_data.profile_id = stored_profile.id
            # 2. Build user relationship with character data
            character_data.generated_by = 1  # Default admin
            # 3. Generate character portrait
            prompt = character_data.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            if portrait_url:
                character_profile.image_url = portrait_url
            else:
                raise Exception("Failed to generate character portrait")

            # 6. Store character data
            stored_character_data = await create_record(session, character_data)

            return JSONResponse(
                content={
                    "profile": stored_profile.model_dump(),
                    "character": stored_character_data.model_dump(),
                    "character_id": stored_character_data.id,
                },
                status_code=201,
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
        )
