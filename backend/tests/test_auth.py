import pytest
import uuid
import time
import base64
from typing import Any, Dict, AsyncGenerator
from fastapi import Request
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from backend.config.settings import AppSettings, get_settings
from backend.services.auth import (
    create_mailer_token,
    create_access_token,
    get_valid_user,
)
from backend.db.db_models import User


@pytest.fixture(scope="module")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_db_session(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_db_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    # Flush and recreate schema before each test
    async with async_db_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
def settings() -> AppSettings:
    return get_settings()


@pytest.fixture(scope="function")
def mock_token_data() -> Dict[str, Any]:
    return {"sub": "1"}


@pytest.fixture(scope="function")
def mock_token(settings: AppSettings, mock_token_data: dict[str, Any]) -> str:
    return create_access_token(
        mock_token_data, settings.secret_key, expires_in_seconds=3600
    )


@pytest.fixture(scope="function")
async def mock_user(async_db_session: AsyncSession) -> User:
    user = User(
        username="AdamOfEternia",
        email="adam@grayskull.com",
        status="active",
        role="user",
    )
    async_db_session.add(user)
    await async_db_session.flush()
    await async_db_session.refresh(user)
    return user


def test_create_mailer_token() -> None:
    token, expiry = create_mailer_token()

    assert isinstance(token, str)
    uuid_obj = uuid.UUID(token)
    assert str(uuid_obj) == token

    now = time.time()
    assert isinstance(expiry, int)
    assert now + 590 <= expiry <= now + 900


def test_create_acess_token(
    settings: AppSettings, mock_token_data: dict[str, Any]
) -> None:

    jwt_encode = create_access_token(mock_token_data, settings.secret_key)

    assert isinstance(jwt_encode, str)
    # Assert JWT format
    parts = jwt_encode.split(".")
    assert len(parts) == 3
    # Ensure each part is base64url-decodable
    for part in parts:
        # Pad the base64 string if necessary
        padding = "=" * (-len(part) % 4)
        try:
            base64.urlsafe_b64decode(part + padding)
        except Exception:
            pytest.fail(f"JWT part is not properly base64url-encoded: {part}")


@pytest.mark.anyio
async def test_get_valid_user(
    async_db_session: AsyncSession,
    settings: AppSettings,
    mock_token: str,
    mock_user: User,
) -> None:
    request = Request(
        {
            "type": "http",
            "headers": [(b"cookie", f"access_token={mock_token}".encode())],
        }
    )

    user = await get_valid_user(async_db_session, settings, request)
    assert user.id == mock_user.id
    assert user.username == "AdamOfEternia"
