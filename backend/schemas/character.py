from pydantic import BaseModel


class NewCharacter(BaseModel):
    id: int | None = None
    image_prompt: str
    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str
    human_relationship: str


class CharacterPatchData(BaseModel):
    image_prompt: str | None = None
    image_url: str | None = None
    generated_by: int | None = None
    name: str | None = None
    planet_name: str | None = None
    planet_description: str | None = None
    personality_traits: str | None = None
    speech_style: str | None = None
    quirks: str | None = None
    human_relationship: str | None = None
