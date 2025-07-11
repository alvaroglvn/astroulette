import pytest
from unittest.mock import patch
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from backend.main import app
from backend.config.session import get_session
from backend.services.auth import assert_admin, get_valid_user
from backend.schemas import NewCharacter, CharacterPatchData
from backend.db.db_models import User


# Fixtures for database and session management
@pytest.fixture(scope="module")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="module")
async def async_db_session(
    async_db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=async_db_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


# Neutral client: unregistered user
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


# Admin client: registered user with admin privileges
@pytest.fixture(scope="function")
async def admin_client(
    async_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_db_session

    async def get_test_admin() -> User:
        return User(
            id=1,
            username="TestAdmin",
            email="admin@admin.com",
            role="admin",
            status="active",
        )

    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[assert_admin] = get_test_admin

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


# User client: registered user with standard privileges
@pytest.fixture(scope="function")
async def user_client(
    async_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
        yield async_db_session

    async def get_test_user() -> User:
        return User(
            id=2,
            username="TestUser",
            email="user@user.com",
            role="user",
            status="active",
        )

    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[get_valid_user] = get_test_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


# Mock character data for testing
@pytest.fixture(scope="function")
def mock_character1() -> NewCharacter:
    return NewCharacter(
        id=1,
        image_prompt="A brave warlord from Mars",
        name="John Carter",
        planet_name="Mars",
        planet_description="Red planet",
        personality_traits="Brave, Loyal",
        speech_style="Formal",
        quirks="Talks like an old timey gentleman",
        human_relationship="Ally and protector",
    )


@pytest.fixture(scope="function")
def mock_character2() -> NewCharacter:
    return NewCharacter(
        id=2,
        image_prompt="A beautiful princess from Mars",
        name="Dejah Thoris",
        planet_name="Mars",
        planet_description="Red planet",
        personality_traits="Intelligent, Strong-willed",
        speech_style="Formal",
        quirks="Loves poetry and literature",
        human_relationship="Lover and confidante",
    )


# Tests
@pytest.mark.order(1)
@pytest.mark.anyio
async def test_generate_character(
    user_client: AsyncClient, mock_character1: NewCharacter
) -> None:
    with (
        patch(
            "backend.routes.rt_characters.generate_character",
            return_value=mock_character1,
        ),
        patch(
            "backend.routes.rt_characters.generate_portrait",
            return_value="https://leonardo.com/alienportrait.png",
        ),
    ):
        response = await user_client.post("/character/generate")
        assert response.status_code == 201
        assert "created and stored" in response.text


@pytest.mark.order(2)
@pytest.mark.anyio
async def test_add_character2(
    admin_client: AsyncClient, mock_character2: NewCharacter
) -> None:
    response = await admin_client.post(
        "/character/add", json=mock_character2.model_dump()
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == mock_character2.name


@pytest.mark.order(3)
@pytest.mark.anyio
async def test_get_character_by_id(
    user_client: AsyncClient, mock_character1: NewCharacter
) -> None:
    character_id = mock_character1.id

    get_response = await user_client.get(url=f"/character/{character_id}")
    assert get_response.status_code == 200
    data = get_response.json()

    assert data["character"]["name"] == "John Carter"
    assert data["character"]["planet_name"] == "Mars"
    assert data["character"]["image_prompt"] == "A brave warlord from Mars"


@pytest.mark.order(4)
@pytest.mark.anyio
async def test_get_all_characters(user_client: AsyncClient) -> None:
    response = await user_client.get("/character")
    assert response.status_code == 200
    data = response.json()
    names = [c["name"] for c in data["characters"]]
    assert "John Carter" in names
    assert "Dejah Thoris" in names


@pytest.mark.order(5)
@pytest.mark.anyio
async def test_get_character_not_found(user_client: AsyncClient) -> None:
    response = await user_client.get("/character/999")
    assert response.status_code == 404


@pytest.mark.order(6)
@pytest.mark.anyio
async def test_update_character(
    admin_client: AsyncClient, mock_character1: NewCharacter
) -> None:
    updates = CharacterPatchData(planet_name="Barsoom")
    response = await admin_client.patch(
        url=f"/character/{mock_character1.id}",
        json=updates.model_dump(exclude_unset=True),
    )
    assert response.status_code == 200
    assert response.json()["planet_name"] == "Barsoom"


# @pytest.mark.order(7)
# @pytest.mark.anyio
# async def test_delete_character(
#     admin_client: AsyncClient, mock_character2: NewCharacter, user_client: AsyncClient
# ) -> None:
#     response = await user_client.get("/character")
#     assert response.status_code == 200
#     data = response.json()
#     print(data)
#     response = await admin_client.delete(f"/character/{mock_character2.id}")
#     assert response.status_code == 200


@pytest.mark.order(8)
@pytest.mark.anyio
async def test_add_character_not_allowed(
    user_client: AsyncClient, mock_character1: NewCharacter
) -> None:
    response = await user_client.post(
        "/character/add", json=mock_character1.model_dump()
    )
    assert response.status_code == 403
    assert (
        response.json()["detail"] == "You don't have permission to perform this action"
    )
