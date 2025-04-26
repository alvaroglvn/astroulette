import logging
import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config.settings import settings_dependency
from app.config.session import db_dependency
from app.services.auth import admin_only_dependency, valid_user_dependency
from app.models import CharacterPatchData
from app.db.db_crud import (
    store_new_character,
    update_record,
    read_all,
    read_record,
    delete_record,
)
from app.db.db_models import Character, Thread
from app.db.db_excepts import DatabaseError, TableNotFound, RecordNotFound
from app.services.openai.character import generate_character
from app.models import NewCharacter
from app.services.leonardo.img_request import generate_portrait
from app.chat_builder import chat_builder

router = APIRouter()

MAX_RETRIES = 3  # Maximum number of retries


@router.post("/character/generate")
async def new_character(
    settings: settings_dependency,
    session: db_dependency,
    user: valid_user_dependency,
) -> JSONResponse:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt} to generate character")

            # 1. Generate new character
            new_character = generate_character(settings.openai_api_key)
            assert new_character is not None

            # 2. Store new character
            stored_character = await store_new_character(session, new_character)
            assert stored_character is not None
            assert isinstance(stored_character.id, int)

            # 3. Generate character portrait
            prompt = stored_character.image_prompt
            portrait_url = await generate_portrait(settings.leonardo_api_key, prompt)

            assert isinstance(stored_character.id, int)

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
    return JSONResponse(
        content={"error": "Unexpected error during character creation."},
        status_code=500,
    )


@router.post("/character/add")
async def add_character(
    session: db_dependency,
    new_character: NewCharacter,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        stored_character = await store_new_character(session, new_character)

        return JSONResponse(content=stored_character.model_dump(), status_code=201)
    except Exception as e:
        return JSONResponse(
            content=f"Unable to create new character: {e}", status_code=500
        )


@router.get("/character")
async def get_all_characters(
    session: db_dependency,
    user: valid_user_dependency,
) -> JSONResponse:
    try:
        characters = await read_all(session, Character)
        if not characters:
            return JSONResponse(content="No characters found", status_code=404)
        result = {"characters": [character.model_dump() for character in characters]}
        return JSONResponse(content=result, status_code=200)
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)


@router.get("/character/chat")
async def load_character(
    session: db_dependency,
    settings: settings_dependency,
    user: valid_user_dependency,
) -> JSONResponse:
    try:
        thread = await chat_builder(session, settings, user)
        assert thread is not None
        assert isinstance(thread, Thread)

        character = await read_record(session, Character, thread.character_id)
        assert character is not None
        assert isinstance(character, Character)

        return JSONResponse(
            content={
                "thread_id": thread.id,
                "character": character.model_dump(),
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to create or load character: {e}"},
            status_code=500,
        )


@router.get("/character/{character_id}")
async def get_character_by_id(
    session: db_dependency,
    character_id: int,
    user: valid_user_dependency,
) -> JSONResponse:
    try:
        character = await read_record(session, Character, character_id)
        if not character:
            return JSONResponse(content="Character not found", status_code=404)

        return JSONResponse(
            content={
                "character": character.model_dump(),
            },
            status_code=200,
        )
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.patch("/character/{character_id}")
async def update_character(
    session: db_dependency,
    character_id: int,
    updates: CharacterPatchData,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        updated = await update_record(
            session, Character, character_id, updates.model_dump(exclude_unset=True)
        )
        if not updated:
            return JSONResponse(content="Character not found", status_code=404)

        return JSONResponse(content=updated.model_dump(), status_code=200)

    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.delete("/character/{character_id}")
async def delete_character(
    session: db_dependency,
    character_id: int,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        await delete_record(session, Character, character_id)

        return JSONResponse(content="Character deleted successfully", status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)
