import time
from app.schemas import NewCharacter
from app.db.db_models import Character, Thread, Message


def character_mapper(new_character: NewCharacter, user_id: int) -> Character:
    character = Character(
        image_prompt=new_character.image_prompt,
        generated_by=user_id,
        name=new_character.name,
        planet_name=new_character.planet_name,
        planet_description=new_character.planet_description,
        personality_traits=new_character.personality_traits,
        speech_style=new_character.speech_style,
        quirks=new_character.quirks,
        human_relationship=new_character.human_relationship,
    )

    return character


def thread_mapper(
    user_id: int,
    character_id: int,
) -> Thread:
    return Thread(
        user_id=user_id,
        character_id=character_id,
        created_at=int(time.time()),
    )


def message_mapper(
    thread_id: int,
    role: str,
    content: str,
) -> Message:
    return Message(
        thread_id=thread_id,
        created_at=int(time.time()),
        role=role,
        content=content,
    )
