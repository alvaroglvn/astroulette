import logging

from app.db.db import DB
from app.db.db_models import *

from app.services.openai.character_gen import character_generator
from app.services.openai.assistant_gen import create_assistant

from app.services.leonardo.leon_models import PhoenixPayload
from app.services.leonardo.img_request import generate_image


async def generate_character(openai_key: str) -> CharacterData:
    """Generates a new character via OpenAI"""
    new_character = await character_generator(openai_key)

    if not new_character:
        logging.error("Failed to create new character.")

    logging.info("New character created.")
    return new_character


def generate_profile(
    openai_key: str, db: DB, new_character: CharacterData
) -> CharacterProfile | None:
    """Generates a new character profile and stores it in the database."""

    # Build character profile
    character_profile = CharacterProfile(
        name=new_character.character_profile.name,
        planet_name=new_character.character_profile.planet_name,
        planet_description=new_character.character_profile.planet_description,
        personality_traits=new_character.character_profile.personality_traits,
        speech_style=new_character.character_profile.speech_style,
        quirks=new_character.character_profile.quirks,
    )

    # Store character profile
    try:
        db.store_entry(character_profile)
    except Exception as e:
        logging.error(f"Failed to store new character profile: {e}")
        return None

    logging.info(f"{character_profile.name} profile stored successfully.")
    return character_profile


async def generate_assistant(
    openai_key: str, db: DB, new_character: CharacterData
) -> Assistant | None:
    """Generates an OpenAI assistant attached to a specific character and stores it in the database."""
    new_assistant = await create_assistant(openai_key, new_character)
    if not new_assistant:
        logging.error("Failed to create new assistant: Invalid response")
        return None

    assistant = Assistant(
        assistant_id=new_assistant.id,
        created_at=new_assistant.created_at,
        name=new_assistant.name,
        model=new_assistant.model,
        instructions=new_assistant.instructions,
        temperature=new_assistant.temperature,
    )
    try:
        db.store_entry(assistant)
    except Exception as e:
        logging.error(f"Failed to store new assistant: {e}")
        return None

    logging.info(f"New assistant {assistant.name} stored in database.")
    return assistant


def generate_character_data(
    openai_key: str, db: DB, character_info: CharacterData, assistant: Assistant
) -> CharacterData | None:
    """Builds and stores new character data"""
    character_data = CharacterData(
        image_prompt=character_info.image_prompt,
        profile_id=character_info.character_profile.profile_id,
        assistant_id=assistant.assistant_id,
    )
    try:
        db.store_entry(character_data)
    except Exception as e:
        logging.error(f"Failed to store new character data: {e}")
        return None

    logging.info(f"{character_data.character_profile.name} stored in database.")
    return character_data


async def generate_portrait(
    leoapi_key: str, db: DB, character_id: int
) -> CharacterData | None:
    """Generates the character's portrait using a previoulsy stored prompt using Leonardo's API, then stores the image url in the database"""

    character = db.read_from_db(CharacterData, "character_id", character_id)

    if not character:
        logging.error("Failed to load character from database.")
        return None

    image_payload = PhoenixPayload(
        prompt=character.image_prompt,
        width=800,
        height=800,
        num_images=1,
        alchemy=False,
        contrast=4,
        enhancePrompt=False,
        styleUUID="8e2bc543-6ee2-45f9-bcd9-594b6ce84",  # Vibrant
        ultra=False,
    )
    image_url = await generate_image(leoapi_key, image_payload)

    if not image_url:
        logging.error("Failed to create portrait: Invalid response.")

    try:
        db.update_db(
            CharacterData, "character_id", character_id, {"image_url": image_url}
        )
    except Exception as e:
        logging.error(f"Failed to store image_url in database: {e}")
        return None

    return CharacterData
