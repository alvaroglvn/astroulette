from typing import Optional
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


class CharacterPatchData(BaseModel):
    image_prompt: Optional[str]
    image_url: Optional[str]
    generated_by: Optional[int]
    name: Optional[str]
    planet_name: Optional[str]
    planet_description: Optional[str]
    personality_traits: Optional[str]
    speech_style: Optional[str]
    quirks: Optional[str]
    human_relationship: Optional[str]
