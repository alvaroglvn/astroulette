from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
import asyncio

from app.dependencies import *
from app.models import *
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
            stored_character = await store_new_character(session, new_character)

            # 3. Generate character portrait
            prompt = stored_character.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            if portrait_url:
                await update_record(
                    session,
                    Character,
                    stored_character.id,
                    {"image_url": portrait_url},
                )
            else:
                raise Exception("Failed to generate character portrait")

            return JSONResponse(
                content=f"{stored_character.name} created and stored.",
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

        character = await read_record(session, Character, character_id)

        return JSONResponse(
            content={
                "character": character.model_dump(),
            },
            status_code=200,
        )
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.get("/characters")
async def get_all_characters(session: db_dependency) -> JSONResponse:
    try:
        characters = await read_all(session, Character)
        result = {"characters": [character.model_dump() for character in characters]}
        return JSONResponse(content=result, status_code=200)
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)


@router.put("/character/{character_id}")
async def upsert_character(
    session: db_dependency, character_id: int, character_data: CharacterFullData
) -> JSONResponse:
    try:
        character_dict = character_data.model_dump()

        updated_character = await update_record(
            session, Character, character_id, character_dict
        )

        logging.info(f"Character {character_id} updated succesfully.")
        return JSONResponse(
            content={
                "character": updated_character.model_dump(),
            },
            status_code=200,
        )
    except RecordNotFound:
        new_character = Character(id=character_id, **character_data)
        stored_character = await create_record(session, new_character)

        logging.info(f"New character {new_character.name} stored.")
        return JSONResponse(
            content={
                "character": stored_character.model_dump(),
            },
            status_code=201,
        )
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.patch("/character/{character_id}")
async def update_character(
    session: db_dependency, character_id: int, updates: CharacterPatchData
) -> JSONResponse:
    try:
        updated = await update_record(
            session, Character, character_id, updates.model_dump(exclude_unset=True)
        )

        return JSONResponse(content=updated.model_dump(), status_code=200)

    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.delete("/character/{character_id}")
async def delete_character(session: db_dependency, character_id: int) -> JSONResponse:
    try:
        await delete_record(session, Character, character_id)

        return JSONResponse(content="Character deleted succesfully", status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)
