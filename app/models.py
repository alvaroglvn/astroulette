from pydantic import BaseModel, EmailStr

# TODO: Feels like these should be in the files (or at least the modules) that use them. E.g. rt_users.py, rt_characters.py, etc. At the very least, it's strange to see them in the root.

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


class UserPatchData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    active: bool | None = None
    login_token: str | None = None
    token_expiry: int | None = None


class MagicLinkRequest(BaseModel):
    email: EmailStr
    username: str
