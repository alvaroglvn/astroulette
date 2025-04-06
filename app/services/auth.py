import uuid
import time
import jwt
from typing import (
    Annotated,
    Optional,
    Tuple,
)
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
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


oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_valid_user(
    session: db_dependency,
    settings: settings_dependency,
    token: Annotated[str, Depends(oath2_scheme)],
) -> User:
    """
    Retrieve and validate the current user from the provided JWT token.

    Args:
        settings: Dependency injection of application settings.
        token (str): The JWT token to validate.

    Raises:
        HTTPException: If the token is invalid or expired.

    Returns:
        User: The user object associated with the token.
    """
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

        user = await read_record(session, User, user_id)
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
