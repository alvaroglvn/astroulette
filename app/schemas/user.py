from pydantic import BaseModel, EmailStr


class UserPatchData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    active: bool | None = None
    login_token: str | None = None
    token_expiry: int | None = None


class MagicLinkRequest(BaseModel):
    email: EmailStr
    username: str
