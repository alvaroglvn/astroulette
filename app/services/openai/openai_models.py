import time

from pydantic import BaseModel, Field
from app.db.db_models import CharacterData, CharacterProfile, Thread, Message


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
    new_character: NewCharacter, user_id: int
) -> tuple[CharacterData, CharacterProfile, Thread]:
    character_data = CharacterData(
        image_prompt=new_character.image_prompt,
        generated_by=user_id,
    )

    character_profile = CharacterProfile(
        image_url=new_character.image_url,
        name=new_character.profile.name,
        planet_name=new_character.profile.planet_name,
        planet_description=new_character.profile.planet_description,
        personality_traits=new_character.profile.personality_traits,
        speech_style=new_character.profile.speech_style,
        quirks=new_character.profile.quirks,
    )

    thread = Thread(
        user_id=user_id,
        character_id=character_data.id,
    )

    return character_data, character_profile, thread


def message_mapper(
    thread_id: int,
    user_id: int,
    character_id: int,
    role: str,
    content: str,
) -> Message:
    return Message(
        thread_id=thread_id,
        user_id=user_id,
        character_id=character_id,
        created_at=time.time(),
        role=role,
        content=content,
    )
