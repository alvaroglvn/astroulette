from typing import AsyncGenerator, Optional
from openai import AsyncOpenAI
from app.db.db_models import Character


async def ai_response(
    openai_api_key: str,
    username: str,
    character: Character,
    user_message: str,
    previous_response_id: Optional[str] = None,
) -> AsyncGenerator:

    client = AsyncOpenAI(
        api_key=openai_api_key,
        project="proj_iHucBz89WXK9PvH3Hqvf5mhf",
    )

    response_stream = await client.responses.create(
        input=user_message,
        model="gpt-4o-mini",
        instructions=f"You are {character.name}, an alien from the planet {character.planet_name}: {character.planet_description}. Your personality is {character.personality_traits}. About your speech style: {character.speech_style}. You also show some quirks: {character.quirks}.",
        max_output_tokens=500,
        previous_response_id=previous_response_id,
        store=True,
        stream=True,
        temperature=1,
        user=username,
    )

    return response_stream
