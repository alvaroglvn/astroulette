import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config.session import get_session


@pytest.fixture(scope="module")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_db_session(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        bind=async_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def async_client(
    async_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_db_session

    app.dependency_overrides[get_session] = get_test_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_add_character(async_client: AsyncClient):
    payload = {
        "image_prompt": "A brave warlord from Mars",
        "generated_by": 1,
        "name": "John Carter",
        "planet_name": "Mars",
        "planet_description": "Red planet",
        "personality_traits": "Brave, Loyal",
        "speech_style": "Formal",
        "quirks": "Talks like an old timey gentleman",
        "human_relationship": "Ally and protector",
    }

    response = await async_client.post("/character/add", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "John Carter"
    assert data["planet_name"] == "Mars"
    assert data["image_prompt"] == "A brave warlord from Mars"
    assert data["image_url"] == "PENDING"
