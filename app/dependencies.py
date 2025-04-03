from typing import AsyncGenerator, Annotated
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_setup import get_async_session
from app.db.db_models import *
from app.db.db_crud import read_record
from app.config import AppSettings


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for the duration of a request.

    Yields:
        AsyncSession: A SQLAlchemy asynchronous session instance.
    """
    async with get_async_session() as session:
        try:
            yield session
        finally:
            await session.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


def get_settings() -> AppSettings:
    """
    Provides an instance of the AppSettings class.

    This function serves as a dependency provider for the application settings, ensuring that an instance of AppSettings is available wherever it is needed.

    Returns:
        AppSettings: An instance of the AppSettings class.
    """
    return AppSettings()


settings_dependency = Annotated[AppSettings, Depends(get_settings)]


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
