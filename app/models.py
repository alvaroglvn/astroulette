from pydantic import BaseModel


class Headers(BaseModel):
    accept: str
    content_type: str
    authorization: str
