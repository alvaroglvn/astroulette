from sqlmodel import Session, select
from app.db.database import CharacterProfile, CharacterData


def store_character(
    new_character: dict, image_url: str, session: Session
) -> CharacterProfile:

    image_prompt = new_character["image_prompt"]

    # Create new character profile
    new_character = CharacterProfile(
        name=new_character["character_profile"]["name"],
        planet_name=new_character["character_profile"]["planet_name"],
        planet_description=new_character["character_profile"]["planet_description"],
        personality_traits=new_character["character_profile"]["personality_traits"],
        speech_style=new_character["character_profile"]["speech_style"],
        quirks=new_character["character_profile"]["quirks"],
    )

    session.add(new_character)
    session.commit()
    session.refresh(new_character)

    # Create CharacterData entry
    character_data = CharacterData(
        image_prompt=image_prompt,
        image_url=image_url,
        character_profile_id=new_character.profile_id,
    )

    session.add(character_data)
    session.commit()

    print(f"New character entry: {new_character.profile_id}, {new_character.name}")

    return new_character
