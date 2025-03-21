from typing import AsyncGenerator
from openai import AsyncOpenAI
from openai.types import A
from app.dependencies import *
from app.db.db_crud import read_record, create_record


async def ai_response(
    user_id: int,
    user_message: str,
    profile_id: int,
    settings: settings_dependency,
    session: db_dependency,
) -> AsyncGenerator:

    user = await read_record(session, User, user_id)
    character = await read_record(session, CharacterProfile, profile_id)

    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
        project="proj_iHucBz89WXK9PvH3Hqvf5mhf",
    )

    response_stream = await client.responses.create(
        input=user_message,
        model="gpt-4o-mini",
        instructions=f"You are {character.name}, an alien from the planet {character.planet_name}: {character.planet_description}. Your personality is {character.personality_traits}. About your speech style: {character.speech_style}. You also show some quirks: {character.quirks}.",
        max_output_tokens=500,
        store=True,
        stream=True,
        temperature=1,
        user=user.username,
    )

    return response_stream
