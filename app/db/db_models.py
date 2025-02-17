from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship

from enum import Enum


# Tables


class CharacterData(SQLModel, table=True):
    character_id: Optional[int] = Field(default=None, primary_key=True)
    image_prompt: str = Field(nullable=False)
    image_url: str = Field(nullable=False, default="PENDING")
    assistant_id: str = Field(nullable=False, foreign_key="assistant.assistant_id")
    profile_id: int = Field(nullable=False, foreign_key="characterprofile.profile_id")
    generated_by: int = Field(
        nullable=False, default=1, foreign_key="user.user_id", index=True
    )

    character_profile: "CharacterProfile" = Relationship(
        back_populates="character_data"
    )
    assistant: "Assistant" = Relationship(back_populates="character_data")
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
        nullable=False, foreign_key="characterdata.character_id", index=True
    )
    assistant_id: str = Field(nullable=False, foreign_key="assistant.assistant_id")

    user: "User" = Relationship(back_populates="threads")
    assistant: Assistant = Relationship(back_populates="threads")
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
    user_name: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, unique=True, index=True)

    characters: List["UserCharacter"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    threads: List["Thread"] = Relationship(back_populates="user", cascade_delete=True)


class UserCharacter(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    character_id: int = Field(
        foreign_key="characterdata.character_id", primary_key=True
    )

    user: User = Relationship(back_populates="characters")
    character_data: CharacterData = Relationship(back_populates="users")
