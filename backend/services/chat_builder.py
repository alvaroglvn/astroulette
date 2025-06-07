import time

from openai import OpenAI

from backend.config.session import db_dependency
from backend.config.clients import openAI_client, LeonardoClient
from backend.services.auth import valid_user_dependency

from backend.db.db_models import Thread, Character
from backend.db.db_crud import (
    fetch_unmet_character,
    store_new_character,
    create_record,
    update_record,
)
from backend.services.openai.character import generate_character_async
from backend.services.leonardo.img_request import generate_portrait


async def chat_builder(
    session: db_dependency,
    user: valid_user_dependency,
    image_client: LeonardoClient,
    text_client: OpenAI = openAI_client,
) -> Thread | None:
    """
    Load chat for the user with a character they have never met:
    a) From the database.
    b) A newly generated character.

    args:
        session: the database session.
        settings: the application settings.
        user: the user object already validated.
    """
    assert isinstance(user.id, int)
    thread: Thread
    # Is there a character the user has not met in the database?

    unmet_character = await fetch_unmet_character(session, user.id)

    # If there is no unmet character, generate a new one
    if not unmet_character:
        # Generate a complete new character
        new_character = await generate_character_async(text_client)
        assert new_character is not None
        # Store generated character in db
        stored_character = await store_new_character(session, new_character, user.id)
        assert stored_character is not None
        # Create the character portrait
        portrait_url = await generate_portrait(
            image_client, stored_character.image_prompt
        )
        # Store the portrait URL in the database
        assert portrait_url is not None and isinstance(portrait_url, str)
        assert stored_character.id is not None and isinstance(stored_character.id, int)
        await update_record(
            session, Character, stored_character.id, {"image_url": portrait_url}
        )

        # Create a new thread beteen the user and the generated character
        assert isinstance(stored_character.id, int)
        thread = Thread(
            user_id=user.id,
            character_id=stored_character.id,
            created_at=int(time.time()),
        )
    else:
        assert unmet_character is not None
        assert isinstance(unmet_character.id, int)

        thread = Thread(
            user_id=user.id,
            character_id=unmet_character.id,
            created_at=int(time.time()),
        )

    # Store the thread in db
    stored_thread = await create_record(session, thread)

    return stored_thread
