from openai import OpenAI
from openai.types.beta.assistant import Assistant

from app.db.db_models import CharacterData, Assistant


def generate_assistant(
    openai_key: str, character_data: CharacterData
) -> Assistant | None:
    """
    Creates an OpenAI assistant with character-specific traits.

    Args:
        openai_key (str): OpenAI API key
        character_data (CharacterData): Character profile data model

    Returns:
        Assistant: Created assistant object or None if creation fails
    """
    client = OpenAI(api_key=openai_key, project="proj_iHucBz89WXK9PvH3Hqvf5mhf")

    name = character_data.character_profile.name
    planet = character_data.character_profile.planet
    planet_description = character_data.character_profile.planet_description
    personality = character_data.character_profile.personality_traits
    speech_style = character_data.character_profile.speech_style
    quirks = character_data.character_profile.quirks

    response = client.beta.assistants.create(
        model="gpt-4o-mini",
        name=name,
        description=f"Fantasy character: {name} from {planet}.",
        temperature=1,
        instructions=f"You are {name}, an alien from  {planet}. Your planet is {planet_description}. Your personality is described as {personality}. Your speech style is described as{speech_style}.Additionally, you have the follwing quirks: {quirks}. Respond as if you are this character.",
        response_format="auto",
    )

    assistant = Assistant(
        assistant_id=response.id,
        created_at=response.created_at,
        name=response.name,
        model=response.model,
        instructions=response.instructions,
        temperature=response.temperature,
    )

    return assistant
