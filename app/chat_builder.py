import time

from app.config.session import db_dependency
from app.config.settings import settings_dependency
from app.services.auth import valid_user_dependency

from app.db.db_models import Thread
from app.db.db_crud import (
    fetch_unmet_character,
    store_new_character,
    create_record,
)
from app.services.openai.character import generate_character_async


async def chat_builder(
    session: db_dependency,
    settings: settings_dependency,
    user: valid_user_dependency,
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
        new_character = await generate_character_async(settings.openai_api_key)
        assert new_character is not None
        # Store generated character in db
        stored_character = await store_new_character(session, new_character)
        assert stored_character is not None

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
