from typing import List, Optional, Iterator

from sqlmodel import Field, Session, SQLModel, create_engine, Relationship

from enum import Enum


# Tables


class CharacterData(SQLModel, table=True):
    character_id: Optional[int] = Field(default=None, primary_key=True)
    image_prompt: str = Field(nullable=False)
    image_url: str = Field(nullable=False)
    assistant_id: str = Field(nullable=False, foreign_key="assistant.assistant_id")
    profile_id: int = Field(nullable=False, foreign_key="characterprofile.profile_id")
    generated_by: int = Field(
        nullable=False, default="Admin", foreign_key="user.user_id", index=True
    )

    character_profile: "CharacterProfile" = Relationship(
        back_populates="character_data", cascade_delete=True
    )
    assistant: "Assistant" = Relationship(
        back_populates="character_data", cascade_delete=True
    )
    users: List["UserCharacter"] = Relationship(back_populates="character_data")


class CharacterProfile(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    planet_name: str = Field(nullable=False)
    planet_description: str = Field(nullable=False)
    personality_traits: str = Field(nullable=False)
    speech_style: str = Field(nullable=False)
    quirks: str = Field(nullable=False)

    character_data: Optional["CharacterData"] = Relationship(
        back_populates="character_profile", cascade_delete=True
    )


class Assistant(SQLModel, table=True):
    assistant_id: str = Field(primary_key=True)
    created_at: int = Field(nullable=False, index=True)
    name: str = Field(nullable=False)
    model: str = Field(nullable=False, index=True)
    instructions: str = Field(nullable=False)
    temperature: float = Field(default=1, index=True)

    character_data: Optional["CharacterData"] = Relationship(
        back_populates="assistant", cascade_delete=True
    )
    threads: List["Thread"] = Relationship(
        back_populates="assistant", cascade_delete=True
    )


class Thread(SQLModel, table=True):
    thread_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: int = Field(nullable=False, index=True)
    user_id: int = Field(nullable=False, foreign_key="user.user_id", index=True)
    character_id: int = Field(
        nullable=False, foreign_key="character_data.character_id", index=True
    )
    assistant_id: str = Field(nullable=False, foreign_key="assistant.assistant_id")

    user: "User" = Relationship(back_populates="threads")
    assistant: Assistant = Relationship(back_populates="threads", cascade_delete=True)
    messages: List["Message"] = Relationship(
        back_populates="thread", cascade_delete=True
    )


class RoleEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    message_id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: int = Field(nullable=False, foreign_key="thread.thread_id", index=True)
    created_at: int = Field(nullable=False, index=True)
    role: RoleEnum = Field(nullable=False, index=True)
    content: str = Field(nullable=False)

    thread: Thread = Relationship(back_populates="messages")


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)

    characters: List["UserCharacter"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    threads: List["Thread"] = Relationship(back_populates="user", cascade_delete=True)


class UserCharacter(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    character_id: int = Field(
        foreign_key="character_data.character_id", primary_key=True
    )

    user: User = Relationship(back_populates="characters", cascade_delete=True)
    character_data: CharacterData = Relationship(
        back_populates="character_data", cascade_delete=True
    )


# Engine
sqlite_file_name = "app/db/alien_talk.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create tables
def create_db_tables() -> None:
    SQLModel.metadata.create_all(engine)


# Create Session
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
