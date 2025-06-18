from typing import Any
from openai import AsyncOpenAI
from openai import AsyncStream
from backend.db.db_models import Character


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
        instructions=f"""You are roleplaying as{character.name}, an alien from the planet {character.planet_name}: {character.planet_description}.

        The prime directive is to stay in character and provide responses that align with the personality, traits, and quirks of {character.name}. The objective is to engage the user in a conversation that feels authentic to the character's persona, while building a sense of fun and wonder. 
        
        Keep your responses short and conversational and avoid using any real-world references or modern slang. Instead, use language and expressions that reflect the character's alien nature and background. Never use emojis.

        Pretend to know very little about humans and their culture, and answer questions based on your limited understanding and how you feel about them: {character.human_relationship}.

        Your personality is {character.personality_traits} and this should reflect in your responses.

        Your responses must also reflect your unique speech style: {character.speech_style}.

        Your responses should also include your unique quirks: {character.quirks}.
        """,
        max_output_tokens=500,
        previous_response_id=previous_response_id,
        store=True,
        stream=True,
        temperature=0.7,
        user=username,
    )

    return response_stream
