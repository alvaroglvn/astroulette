from typing import Any
from openai import AsyncOpenAI
from openai import AsyncStream
from app.db.db_models import Character


async def ai_response(
    openai_api_key: str,
    username: str,
    character: Character,
    user_message: str,
    previous_response_id: str | None = None,
) -> AsyncStream[Any]:
    client = AsyncOpenAI(
        api_key=openai_api_key,
        project="proj_iHucBz89WXK9PvH3Hqvf5mhf",
    )

    response_stream = await client.responses.create(
        input=user_message,
        model="gpt-4o",
        instructions=f"You are {character.name}, an alien from the planet {character.planet_name}: {character.planet_description}. Your personality is {character.personality_traits}. About your speech style: {character.speech_style}. Your speech also shows your unique quirks: {character.quirks}. You have very limited information about humans, so answer every question accordingly. About humans, this describes your feelings: {character.human_relationship}. Your answers should be conversational, short, and not overly verbose.",
        max_output_tokens=500,
        previous_response_id=previous_response_id,
        store=True,
        stream=True,
        temperature=1,
        user=username,
    )

    return response_stream
