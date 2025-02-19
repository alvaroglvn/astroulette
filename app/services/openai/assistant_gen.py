from openai import OpenAI
from openai.types.beta.assistant import Assistant
from app.services.openai.openai_models import *


def create_assistant(openai_key: str, character_data: dict) -> Assistant | None:
    client = OpenAI(api_key=openai_key, project="proj_iHucBz89WXK9PvH3Hqvf5mhf")

    name, planet, planet_description, personality, speech_style, quirks = (
        character_data["character_profile"]["name"],
        character_data["character_profile"]["planet"],
        character_data["character_profile"]["planet_description"],
        character_data["character_profile"]["personality_traits"],
        character_data["character_profile"]["speech_style"],
        character_data["character_profile"]["quirks"],
    )

    assistant = client.beta.assistants.create(
        model="gpt-4o-mini",
        name=name,
        description=f"Fantasy character: {name} from {planet}.",
        temperature=1,
        instructions=f"You are {name}, an alien from  {planet}. Your planet is {planet_description}. Your personality is described as {personality}. Your speech style is described as{speech_style}.Additionally, you have the follwing quirks: {quirks}. Respond as if you are this character.",
        response_format="auto",
    )

    validated_response = openai_resp_validator(Assistant, assistant)

    if validated_response:
        return validated_response
