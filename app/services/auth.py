import uuid
import time
import jwt
from typing import Optional, Tuple


def create_mailer_token() -> Tuple[str, int]:
    """
    Create a temporary token for mailer verification.

    Generates a unique UUID token and sets an expiry time 10 minutes
    (600 seconds) from the current time.

    Returns:
        tuple[str, int]: A tuple containing the generated token and its expiry timestamp.
    """
    token = str(uuid.uuid4())
    expiry = int(time.time()) + 600  # ten minutes
    return token, expiry


def create_access_token(
    data: dict, secret_key: str, expires_in_seconds: Optional[int] = None
) -> str:
    """
    Create a JWT access token.

    This function generates a JWT token with an expiration time. The token payload
    is the copy of the provided data and the expiration time is added under the key "exp".

    Args:
        data (dict): Data to encode in the token.
        secret_key (str): Secret key to sign the token.
        expires_in_seconds (Optional[int]): Token expiration time in seconds (default is 3600 seconds).

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    expire = int(time.time()) + (expires_in_seconds or 3600)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")
