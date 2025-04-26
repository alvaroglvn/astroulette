import uuid
import time
import jwt
from typing import (
    Annotated,
    Tuple,
    Any,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
    Request,
)
from app.config.settings import settings_dependency
from app.config.session import db_dependency
from app.db.db_models import User
from app.db.db_crud import read_record


def create_mailer_token() -> Tuple[str, int]:
    """
    Create a temporary token for mailer verification.

    Generates a unique UUID token and sets an expiry time 10 minutes
    (600 seconds) from the current time.

    Returns:
        tuple[str, int]: A tuple containing the generated token and its expiry timestamp.
    """
    token = str(uuid.uuid4())
    expiry = int(time.time()) + 900  # ten minutes
    return token, expiry


def create_access_token(
    data: dict[str, Any], secret_key: str, expires_in_seconds: int | None = None
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
    return jwt.encode(to_encode, secret_key, algorithm="HS256")  # type: ignore


async def get_valid_user(
    session: db_dependency,
    settings: settings_dependency,
    request: Request,
) -> User:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])  # type: ignore
        user_id = payload.get("sub")
        if not str(user_id).isdigit():
            raise credential_exception
        user_id = int(user_id)

        user = await read_record(session, User, user_id)
        if user is None:
            raise credential_exception
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credential_exception


valid_user_dependency = Annotated[User, Depends(get_valid_user)]


# Admin only privileges
def assert_admin(user: valid_user_dependency) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action",
        )
    return user


admin_only_dependency = Annotated[User, Depends(assert_admin)]
