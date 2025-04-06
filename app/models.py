from typing import Optional
from pydantic import BaseModel, EmailStr


class NewCharacter(BaseModel):
    id: int = None
    image_prompt: str
    name: str
    planet_name: str
    planet_description: str
    personality_traits: str
    speech_style: str
    quirks: str
    human_relationship: str


class CharacterPatchData(BaseModel):
    image_prompt: Optional[str] = None
    image_url: Optional[str] = None
    generated_by: Optional[int] = None
    name: Optional[str] = None
    planet_name: Optional[str] = None
    planet_description: Optional[str] = None
    personality_traits: Optional[str] = None
    speech_style: Optional[str] = None
    quirks: Optional[str] = None
    human_relationship: Optional[str] = None


class UserPatchData(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    login_token: Optional[str] = None
    token_expiry: Optional[int] = None


class MagicLinkRequest(BaseModel):
    email: EmailStr
    username: str
