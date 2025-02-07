from pydantic import BaseModel


class Headers(BaseModel):
    accept: str
    content_type: str
    authorization: str


class NewCharacterProfile(BaseModel):
    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str


class NewCharacterRequest(BaseModel):
    character_profile: NewCharacterProfile
    image_prompt: str
    image_url: str
