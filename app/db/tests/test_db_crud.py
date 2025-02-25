from typing import Optional, List, Dict, Any, AsyncGenerator
import pytest
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from app.db.db_models import CharacterData, UserCharacters
from app.db.db_crud import (
    create_record,
    read_record,
    read_all,
    update_record,
    delete_record,
    fetch_unmet_character,
)

DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with async_session() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_record(session: AsyncSession) -> None:
    character: CharacterData = CharacterData(name="Test Character")
    result: Optional[CharacterData] = await create_record(session, character)
    assert result is not None
    assert result.id is not None


@pytest.mark.asyncio
async def test_read_record(session: AsyncSession) -> None:
    character: CharacterData = CharacterData(name="Test Character")
    await create_record(session, character)
    result: Optional[CharacterData] = await read_record(
        session, CharacterData, character.id
    )
    assert result is not None
    assert result.id == character.id


@pytest.mark.asyncio
async def test_read_all(session: AsyncSession) -> None:
    character1: CharacterData = CharacterData(name="Test Character 1")
    character2: CharacterData = CharacterData(name="Test Character 2")
    await create_record(session, character1)
    await create_record(session, character2)
    results: List[CharacterData] = await read_all(session, CharacterData)
    assert len(results) == 2


@pytest.mark.asyncio
async def test_update_record(session: AsyncSession) -> None:
    character: CharacterData = CharacterData(name="Test Character")
    await create_record(session, character)
    updates: Dict[str, Any] = {"name": "Updated Character"}
    result: Optional[CharacterData] = await update_record(
        session, CharacterData, character.id, updates
    )
    assert result is not None
    assert result.name == "Updated Character"


@pytest.mark.asyncio
async def test_delete_record(session: AsyncSession) -> None:
    character: CharacterData = CharacterData(name="Test Character")
    await create_record(session, character)
    result: bool = await delete_record(session, CharacterData, character.id)
    assert result is True
    deleted_record: Optional[CharacterData] = await read_record(
        session, CharacterData, character.id
    )
    assert deleted_record is None


@pytest.mark.asyncio
async def test_fetch_unmet_character(session: AsyncSession) -> None:
    character: CharacterData = CharacterData(name="Test Character")
    await create_record(session, character)
    user_character: UserCharacters = UserCharacters(
        user_id=1, character_id=character.id
    )
    await create_record(session, user_character)
    result: Optional[CharacterData] = await fetch_unmet_character(session, 1)
    assert result is None
