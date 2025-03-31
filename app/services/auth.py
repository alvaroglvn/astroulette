from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import uuid
import time

from app.dependencies import settings_dependency


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


oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_valid_user(
    settings: settings_dependency,
    token: str = Depends(oath2_scheme),
) -> str:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credential_exception
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise credential_exception
