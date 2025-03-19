from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
import asyncio

from app.dependencies import *
from app.db.db_crud import *
from app.db.db_models import *
from app.db.db_excepts import *
from app.db.db_utils import *
from app.services.openai.character import generate_character
from app.services.openai.openai_models import char_data_mapper
from app.services.leonardo.img_request import generate_portrait

router = APIRouter()

MAX_RETRIES = 3  # Maximum number of retries


@router.post("/generate-character")
async def new_character(
    settings: settings_dependency,
    session: db_dependency,
) -> JSONResponse:

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt} to generate character")

            # Start transaction manually
            await session.begin()

            # 1. Generate new character
            new_character = generate_character(settings.openai_api_key)

            # 2. Map character data for storage
            character_data, character_profile, thread = char_data_mapper(new_character)

            # 2a. Store character profile
            stored_profile = await create_record(session, character_profile)
            character_data.profile_id = stored_profile.id

            # 2b. Store character data
            stored_character_data = await create_record(session, character_data)

            # 2c. Store thread data
            thread.character_id = stored_character_data.id
            stored_thread = await create_record(session, thread)

            # 3. Generate character portrait
            prompt = stored_character_data.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            if portrait_url:
                stored_profile.image_url = portrait_url
                await session.commit()  # Commit all changes if successful
            else:
                raise Exception("Failed to generate character portrait")

            logging.info("Character successfully created")
            return JSONResponse(
                content={
                    "data": stored_character_data.model_dump(),
                    "profile": stored_profile.model_dump(),
                    "thread": stored_thread.model_dump(),
                },
                status_code=201,
            )

        except Exception as e:
            logging.error(f"Error on attempt {attempt}: {e}")
            await session.rollback()  # Rollback changes if an error occurs

            if attempt < MAX_RETRIES:
                logging.info(f"Retrying character creation (Attempt {attempt + 1})...")
                await asyncio.sleep(1)  # Small delay before retrying
            else:
                logging.error("Max retries reached. Failing character creation.")
                return JSONResponse(
                    content={
                        "error": "Character creation failed after multiple attempts."
                    },
                    status_code=500,
                )

        finally:
            # Ensure session is always closed
            await session.close()
            logging.info("Session closed to prevent memory leaks")
