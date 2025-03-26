from pydantic import BaseModel


class CharacterFullData(BaseModel):
    image_prompt: str
    image_url: str
    generated_by: int
    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str
    human_relationship: str
