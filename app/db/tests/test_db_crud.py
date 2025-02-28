from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import time

from app.db.db_models import *
from app.db.db_crud import *
from app.db.db_excepts import RecordNotFound

# Test database URL
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


@pytest_asyncio.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture(name="mock_user")
async def mock_user_fixture() -> User:
    user = User(username="test_user", email="test@example.com", active=True)
    return user


@pytest_asyncio.fixture(name="mock_assistant")
async def mock_assistant_fixture() -> Assistant:
    assistant = Assistant(
        assistant_id="test_assistant_id",
        created_at=int(time.time()),
        name="Test Assistant",
        model="gpt-4",
        instructions="Test instructions",
        temperature=0.7,
    )
    return assistant


@pytest_asyncio.fixture(name="mock_character_profile")
async def mock_character_profile_fixture() -> CharacterProfile:
    profile = CharacterProfile(
        name="Test Character",
        planet_name="Test Planet",
        planet_description="A test planet description",
        personality_traits="Friendly, Helpful",
        speech_style="Formal",
        quirks="Always says 'beep' at the end of sentences",
    )
    return profile


@pytest_asyncio.fixture(name="mock_character_data")
async def mock_character_data_fixture(
    mock_user: User,
    mock_assistant: Assistant,
    mock_character_profile: CharacterProfile,
) -> CharacterData:
    character_data = CharacterData(
        image_prompt="A test image prompt",
        image_url="PENDING",
        profile_id=mock_character_profile.id,
        assistant_id=mock_assistant.assistant_id,
        generated_by=mock_user.id,
    )
    return character_data


@pytest_asyncio.fixture(name="mock_user_character")
async def mock_user_character_fixture(
    mock_user: User,
    mock_character_data: CharacterData,
) -> UserCharacters:
    user_character = UserCharacters(
        user_id=mock_user.id, character_id=mock_character_data.id
    )
    return user_character


@pytest_asyncio.fixture(name="mock_thread")
async def mock_thread_fixture(
    mock_user: User,
    mock_character_data: CharacterData,
    mock_assistant: Assistant,
) -> Thread:
    thread = Thread(
        created_at=int(time.time()),
        user_id=mock_user.id,
        character_id=mock_character_data.id,
        assistant_id=mock_assistant.assistant_id,
    )
    return thread


@pytest_asyncio.fixture(name="mock_message")
async def mock_message_fixture(
    mock_thread: Thread,
) -> Message:
    message = Message(
        thread_id=mock_thread.id,
        created_at=int(time.time()),
        role="user",
        content="Test message content",
    )
    return message


@pytest.mark.asyncio
async def test_create_record(
    session: AsyncSession,
    mock_user: User,
    mock_assistant: Assistant,
    mock_character_profile: CharacterProfile,
    mock_character_data: CharacterData,
    mock_user_character: UserCharacters,
    mock_thread: Thread,
    mock_message: Message,
) -> None:
    # Create user
    user_result = await create_record(session, mock_user)
    assert user_result is not None
    assert user_result.username == "test_user"
    assert user_result.email == "test@example.com"
    assert user_result.active is True

    # Create assistant
    assistant_result = await create_record(session, mock_assistant)
    assert assistant_result is not None
    assert assistant_result.assistant_id == "test_assistant_id"
    assert assistant_result.name == "Test Assistant"
    assert assistant_result.model == "gpt-4"
    assert assistant_result.instructions == "Test instructions"
    assert assistant_result.temperature == 0.7
    assert isinstance(assistant_result.created_at, int)

    # Create character profile
    profile_result = await create_record(session, mock_character_profile)
    assert profile_result is not None
    assert profile_result.name == "Test Character"
    assert profile_result.planet_name == "Test Planet"
    assert profile_result.planet_description == "A test planet description"
    assert profile_result.personality_traits == "Friendly, Helpful"
    assert profile_result.speech_style == "Formal"
    assert profile_result.quirks == "Always says 'beep' at the end of sentences"

    # Create character data
    mock_character_data.profile_id = profile_result.id
    mock_character_data.generated_by = user_result.id
    character_data_result = await create_record(session, mock_character_data)
    assert character_data_result is not None
    assert character_data_result.image_prompt == "A test image prompt"
    assert character_data_result.image_url == "PENDING"
    assert character_data_result.profile_id == profile_result.id
    assert character_data_result.assistant_id == mock_assistant.assistant_id
    assert character_data_result.generated_by == user_result.id

    # Create user-character association
    mock_user_character.user_id = user_result.id
    mock_user_character.character_id = character_data_result.id
    user_character_result = await create_record(session, mock_user_character)
    assert user_character_result is not None
    assert user_character_result.user_id == user_result.id
    assert user_character_result.character_id == character_data_result.id

    # Create thread
    mock_thread.user_id = user_result.id
    mock_thread.character_id = character_data_result.id
    thread_result = await create_record(session, mock_thread)
    assert thread_result is not None
    assert thread_result.user_id == user_result.id
    assert thread_result.character_id == character_data_result.id
    assert thread_result.assistant_id == mock_assistant.assistant_id
    assert isinstance(thread_result.created_at, int)

    # Create message
    mock_message.thread_id = thread_result.id
    message_result = await create_record(session, mock_message)
    assert message_result is not None
    assert message_result.thread_id == thread_result.id
    assert message_result.role == "user"
    assert message_result.content == "Test message content"


@pytest.mark.asyncio
async def test_read_record(session: AsyncSession, mock_user: User) -> None:
    # Create user
    user_result = await create_record(session, mock_user)
    assert user_result is not None
    # Read user
    read_user = await read_record(session, User, user_result.id)
    assert read_user is not None
    assert read_user.username == "test_user"
    assert read_user.email == "test@example.com"
    assert read_user.active is True


@pytest.mark.asyncio
async def test_read_all_records(session: AsyncSession, mock_user: User) -> None:
    # Create user
    user_result = await create_record(session, mock_user)
    assert user_result is not None
    # Read all users
    users = await read_all(session, User)
    assert len(users) > 0
    assert any(user.id == user_result.id for user in users)


@pytest.mark.asyncio
async def test_update_record(session: AsyncSession, mock_user: User) -> None:
    # Create user
    user_result = await create_record(session, mock_user)
    assert user_result is not None
    # Update user
    updates = {
        "username": "updated_user",
        "email": "updated@example.com",
        "active": False,
    }
    updated_user = await update_record(session, User, user_result.id, updates)
    assert updated_user is not None
    assert updated_user.username == "updated_user"
    assert updated_user.email == "updated@example.com"
    assert updated_user.active is False


@pytest.mark.asyncio
async def test_delete_record(session: AsyncSession, mock_user: User) -> None:
    # Create user
    user_result = await create_record(session, mock_user)
    assert user_result is not None
    # Delete user
    await delete_record(session, User, user_result.id)
    # Try to read deleted user and expect a RecordNotFound exception
    with pytest.raises(RecordNotFound):
        await read_record(session, User, user_result.id)


@pytest.mark.asyncio
async def test_fetch_unmet_character(
    session: AsyncSession,
    mock_user: User,
    mock_assistant: Assistant,
    mock_character_profile: CharacterProfile,
) -> None:
    # Create user
    user = await create_record(session, mock_user)
    assert user is not None

    # Create assistant
    assistant = await create_record(session, mock_assistant)
    assert assistant is not None

    # Create character profile
    profile = await create_record(session, mock_character_profile)
    assert profile is not None

    # Create two character data entries
    character1 = CharacterData(
        image_prompt="Test prompt 1",
        image_url="PENDING",
        profile_id=profile.id,
        assistant_id=assistant.assistant_id,
        generated_by=user.id,
    )
    character2 = CharacterData(
        image_prompt="Test prompt 2",
        image_url="PENDING",
        profile_id=profile.id,
        assistant_id=assistant.assistant_id,
        generated_by=user.id,
    )

    char1 = await create_record(session, character1)
    char2 = await create_record(session, character2)
    assert char1 is not None
    assert char2 is not None

    # Associate character1 with the user
    user_char = UserCharacters(user_id=user.id, character_id=char1.id)
    await create_record(session, user_char)

    # Test fetch_unmet_character
    unmet = await fetch_unmet_character(session, user.id)
    assert unmet is not None
    assert unmet.id == char2.id  # Should get character2 as it's unmet

    # Associate character2 with the user
    user_char2 = UserCharacters(user_id=user.id, character_id=char2.id)
    await create_record(session, user_char2)

    # Test fetch_unmet_character again
    unmet = await fetch_unmet_character(session, user.id)
    assert unmet is None  # Should get None as all characters are met
