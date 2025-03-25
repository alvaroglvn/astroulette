from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
import asyncio

from app.dependencies import *
from app.models import CharacterFullData
from app.db.db_crud import *
from app.db.db_models import *
from app.db.db_excepts import *
from app.db.db_utils import *
from app.services.openai.character import generate_character
from app.services.leonardo.img_request import generate_portrait

router = APIRouter()

MAX_RETRIES = 3  # Maximum number of retries


@router.post("/character/generate")
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

            # 2. Store new character
            stored_profile, stored_character_data = await store_new_character(
                session, settings.openai_api_key, new_character
            )

            # 3. Generate character portrait
            prompt = stored_character_data.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            if portrait_url:
                await update_record(
                    session,
                    CharacterProfile,
                    stored_profile.id,
                    {"image_url": portrait_url},
                )
            else:
                raise Exception("Failed to generate character portrait")

            return JSONResponse(
                content=f"{stored_profile.name} created and stored.",
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


@router.get("/character/{character_id}")
async def character_info(session: db_dependency, character_id: int) -> JSONResponse:
    try:

        character_data = await read_record(session, CharacterData, character_id)
        character_profile = await read_record(session, CharacterProfile, character_id)

        return JSONResponse(
            content={
                "character": {character_data.model_dump()},
                "character_profile": character_profile.model_dump(),
            },
            status_code=200,
        )
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.put("/character/{character_id}")
async def character_upsert(
    session: db_dependency, character_id: int, character: CharacterFullData
) -> JSONResponse:
    try:
        character_profile = character.model_dump(
            exclude={"image_prompt", "generated_by"}
        )
        character_data = {
            "image_promt": character.image_prompt,
            "generated_by": character.generated_by,
            "profile_id": character_id,
        }

        updated_profile = await update_record(
            session, CharacterProfile, character_id, character_profile
        )
        updated_data = await update_record(
            session, CharacterData, character_id, character_data
        )

        logging.info(f"Character {character_id} updated succesfully.")
        return JSONResponse(
            content={
                "character_data": updated_data.model_dump(),
                "character_profile": updated_profile.model_dump(),
            },
            status_code=200,
        )
    except RecordNotFound:
        new_profile = CharacterProfile(id=character_id, **character_profile)
        stored_profile = await create_record(session, new_profile)

        new_char_data = CharacterData(
            id=character_id,
            profile_id=character_id,
            image_prompt=character.image_prompt,
            generated_by=character.generated_by,
        )
        stored_char_data = await create_record(session, new_char_data)

        logging.info(f"New character {character.name} stored.")
        return JSONResponse(
            content={
                "character_data": stored_char_data.model_dump(),
                "character_profile": stored_profile.model_dump(),
            },
            status_code=201,
        )
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.delete("/character/{character_id}")
async def delete_character(session: db_dependency, character_id: int) -> JSONResponse:
    try:
        await delete_record(session, CharacterData, character_id)

        return JSONResponse(content="Character deleted succesfully", status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)
