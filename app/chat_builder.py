from app.dependencies import *
from app.db.db_crud import fetch_unmet_character, store_new_character, create_record
from app.services.openai.character import generate_character_async


async def chat_builder(
    session: db_dependency,
    settings: settings_dependency,
    user: valid_user_dependency,
):
    """
    Load chat for the user with a character they have never met:
    a) From the database.
    b) A newly generated character.

    args:
        session: the database session.
        settings: the application settings.
        user: the user object already validated.
    """
    # Is there a character the user has not met in the database?
    unmet_character = await fetch_unmet_character(session, user.id)
    # Create a new thread beteen the user and the unmet character
    thread = Thread(
        user_id=user.id,
        character_id=unmet_character.id,
        created_at=time.time(),
    )

    if not unmet_character:
        # Generate a complete new character
        new_character = await generate_character_async(settings.openai_api_key)
        # Store generated character in db
        stored_character = await store_new_character(session, new_character)

        # Create a new thread beteen the user and the generated character
        thread = Thread(
            user_id=user.id,
            character_id=stored_character.id,
            created_at=time.time(),
        )

    # Store the thread in db
    stored_thread = await create_record(session, thread)
