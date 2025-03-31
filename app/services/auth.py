from typing import Optional
import jwt
import uuid
import time


def create_mailer_token() -> tuple[str, int]:
    token = str(uuid.uuid4())
    expiry = int(time.time()) + 600  # ten minutes

    return token, expiry


def create_access_token(
    data: dict, secret_key: str, expires_in_seconds: Optional[int]
) -> str:
    to_encode = data.copy()
    expire = int(time.time()) + (expires_in_seconds or 3600)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")
