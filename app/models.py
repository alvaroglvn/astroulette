from pydantic import BaseModel
from typing import Optional


class Headers(BaseModel):
    accept: str
    content_type: str
    authorization: str
