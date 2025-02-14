from typing import Generator
import time

import pytest
from sqlmodel import Session
from app.db.db import DB
from app.db.db_models import *


# TEST DATABASE SETUP #


@pytest.fixture(scope="session")
def db_instance() -> Generator:
    """Creates a test database instance"""
    db = DB(filepath=":memory:")
    yield db


@pytest.fixture(scope="session")
def session(db_instance: DB) -> Generator:
    """Creates a test session wih the database"""
    with Session(db_instance.engine) as session:
        yield session


# Reset database before new test
@pytest.fixture(autouse=True, scope="function")
def reset_db(session: Session) -> Generator:
    SQLModel.metadata.drop_all(session.bind)
    SQLModel.metadata.create_all(session.bind)
    yield


# MOCKUP DATA SETUP #


@pytest.fixture()
def mockup_user(db_instance: DB) -> User:
    mockup_user = User(
        user_name="William Ryker",
        email="williamryker@staracademy.org",
    )
    db_instance.store_entry(mockup_user)
    return mockup_user


@pytest.fixture()
def mockup_profile(db_instance: DB) -> CharacterProfile:
    mockup_profile = CharacterProfile(
        name="Glorb",
        planet_name="Banana Prime",
        planet_description="A tropical jungle paradise",
        personality_traits="Friendly and kooky.",
        speech_style="Talks excitedly and fast",
        quirks="Uses old-timey expressions",
    )
    db_instance.store_entry(mockup_profile)
    return mockup_profile


@pytest.fixture()
def mockup_assistant(db_instance: DB) -> Assistant:
    mockup_assistant = Assistant(
        assistant_id="glorb_assistant_1",
        created_at=int(time.time()),
        name="Glorb",
        model="gpt-4o",
        instructions="You are Glorb the alien.",
        temperature=1,
    )
    db_instance.store_entry(mockup_assistant)
    return mockup_assistant


@pytest.fixture()
def mockup_character(
    db_instance: DB,
    mockup_profile: CharacterProfile,
    mockup_assistant: Assistant,
    mockup_user: User,
) -> CharacterData:
    mockup_character = CharacterData(
        image_prompt="A jolly alien with a monocle.",
        image_url="http://mockupalien.test",
        assistant_id=mockup_assistant.assistant_id,
        profile_id=mockup_profile.profile_id,
        generated_by=mockup_user.user_id,
    )
    db_instance.store_entry(mockup_character)
    return mockup_character


@pytest.fixture()
def mockup_thread(
    db_instance: DB,
    mockup_user: User,
    mockup_character: CharacterData,
    mockup_assistant: Assistant,
) -> Thread:
    mockup_thread = Thread(
        created_at=time.time(),
        user_id=mockup_user.user_id,
        character_id=mockup_character.character_id,
        assistant_id=mockup_assistant.assistant_id,
    )
    db_instance.store_entry(mockup_thread)
    return mockup_thread()


@pytest.fixture()
def mockup_message(
    db_instance: DB,
    mockup_thread: Thread,
) -> Message:
    mockup_message = Message(
        thread_id=mockup_thread.thread_id,
        created_at=int(time.time()),
        role="assistant",
        content="Hello, my name is Glorb",
    )
    db_instance.store_entry(mockup_message)
    return mockup_message


# TESTS #


# Store in DB
def test_storage(mockup_character: CharacterData) -> None:
    assert mockup_character.image_url == "http://mockupalien.test"
    assert mockup_character.assistant_id is not None
    assert mockup_character.profile_id is not None
    assert mockup_character.generated_by is not None


# Read from DB
def test_read(db_instance: DB, mockup_character: CharacterData) -> None:
    character = db_instance.read_from_db(
        CharacterData, "character_id", mockup_character.character_id
    )
    assert character.image_prompt == "A jolly alien with a monocle."


# Update DB
def test_update(db_instance: DB, mockup_character: CharacterData) -> None:
    db_instance.update_db(
        CharacterData,
        "character_id",
        mockup_character.character_id,
        {"image_url": "http://new-image.test"},
    )
    updated = db_instance.read_from_db(
        CharacterData, "character_id", mockup_character.character_id
    )
    assert updated.image_url == "http://new-image.test"


# Delete from DB
def test_delete(db_instance: DB, mockup_character: CharacterData) -> None:
    db_instance.delete_character(mockup_character.character_id)
    with pytest.raises(LookupError):
        db_instance.read_from_db(
            CharacterData, "character_id", mockup_character.character_id
        )
