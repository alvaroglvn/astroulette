from pydantic import BaseModel

from app.db.db_models import CharacterProfile, Assistant


class Headers(BaseModel):
    accept: str
    content_type: str
    authorization: str


class CharacterResponse(BaseModel):
    character_profile: CharacterProfile
    assistant: Assistant
    image_url: str
