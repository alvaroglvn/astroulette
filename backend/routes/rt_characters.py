import logging
import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.config.settings import settings_dependency
from backend.config.session import db_dependency
from backend.services.auth import admin_only_dependency, valid_user_dependency
from backend.schemas import CharacterPatchData, NewCharacter
from backend.db.db_crud import (
    store_new_character,
    update_record,
    read_all,
    read_record,
    delete_record,
)
from backend.db.db_models import Character, Thread
from backend.db.db_excepts import DatabaseError, TableNotFound, RecordNotFound
from backend.services.openai.character import generate_character
from backend.services.leonardo.img_request import generate_portrait
from backend.services.chat_builder import chat_builder
from backend.utils.retry import retry_async

router = APIRouter()


@router.post("/character/generate")
@retry_async(3, 1.0)
async def new_character(
    settings: settings_dependency,
    session: db_dependency,
    user: valid_user_dependency,
) -> JSONResponse:

    new_char = generate_character(settings.openai_api_key)

    assert isinstance(new_char, NewCharacter)
    assert isinstance(user.id, int)
    stored = await store_new_character(session, new_char, user.id)

    url = await generate_portrait(settings.leonardo_api_key, stored.image_prompt)

    if not url:
        raise RuntimeError("portrait failed")

    assert isinstance(stored.id, int)
    await update_record(session, Character, stored.id, {"image_url": url})

    return JSONResponse(content=f"{stored.name} created and stored.", status_code=201)


@router.post("/character/add")
async def add_character(
    session: db_dependency,
    new_character: NewCharacter,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        assert admin.id is not None
        stored_character = await store_new_character(session, new_character, admin.id)

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
        logging.error(traceback.format_exc())
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
