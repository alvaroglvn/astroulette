import time
from app.models import NewCharacter
from app.db.db_models import Character, Thread, Message


def character_mapper(
    new_character: NewCharacter, user_id: int = 1
) -> tuple[Character, Thread]:
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

    thread = Thread(
        user_id=user_id,
        character_id=new_character.id,
        created_at=time.time(),
    )

    return character, thread


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
