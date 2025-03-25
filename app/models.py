from pydantic import BaseModel


class CharacterFullData(BaseModel):
    # Data for CharacterData
    image_prompt: str
    profile_id: int
    generated_by: int
    # Data for CharacterProfile
    image_url: str
    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str
