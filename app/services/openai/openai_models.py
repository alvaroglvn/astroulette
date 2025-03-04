from pydantic import BaseModel, Field
from openai.types.beta.assistant import Assistant
from app.db.db_models import CharacterData, CharacterProfile, DBAssistant


class NewProfile(BaseModel):
    name: str = Field()
    planet_name: str = Field()
    planet_description: str = Field()
    personality_traits: str = Field()
    speech_style: str = Field()
    quirks: str = Field()


class NewCharacter(BaseModel):
    image_prompt: str = Field()
    image_url: str = Field()
    profile: NewProfile = Field()


def char_data_mapper(
    new_character: NewCharacter,
) -> tuple[CharacterData, CharacterProfile]:
    character_data = CharacterData(
        image_prompt=new_character.image_prompt, image_url=new_character.image_url
    )

    character_profile = CharacterProfile(
        name=new_character.profile.name,
        planet_name=new_character.profile.planet_name,
        planet_description=new_character.profile.planet_description,
        personality_traits=new_character.profile.personality_traits,
        speech_style=new_character.profile.speech_style,
        quirks=new_character.profile.quirks,
    )

    return character_data, character_profile


def assistant_data_mapper(assistant: Assistant) -> DBAssistant:
    return DBAssistant(
        assistant_id=assistant.id,
        created_at=assistant.created_at,
        name=assistant.name,
        model=assistant.model,
        instructions=assistant.instructions,
        temperature=assistant.temperature,
    )
