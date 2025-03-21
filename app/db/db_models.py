from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
import time


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, unique=True, index=True)
    active: bool = Field(nullable=False, default=True, index=True)

    character_data: List["CharacterData"] = Relationship(back_populates="user")
    user_characters: List["UserCharacters"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    messages: List["Message"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    threads: List["Thread"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class CharacterProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    image_url: str = Field(default="PENDING")
    name: str = Field(nullable=False, index=True)
    planet_name: str = Field(nullable=False)
    planet_description: str = Field(nullable=False)
    personality_traits: str = Field(nullable=False)
    speech_style: str = Field(nullable=False)
    quirks: str = Field(nullable=False)

    character_data: Optional["CharacterData"] = Relationship(back_populates="profile")

    threads: List["Thread"] = Relationship(
        back_populates="character",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    messages: List["Message"] = Relationship(
        back_populates="character",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class CharacterData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    image_prompt: str = Field(nullable=False)

    profile_id: int = Field(foreign_key="characterprofile.id")
    generated_by: int = Field(foreign_key="user.id")

    profile: Optional[CharacterProfile] = Relationship(
        back_populates="character_data",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "single_parent": True},
    )

    user: Optional[User] = Relationship(back_populates="character_data")
    user_characters: List["UserCharacters"] = Relationship(
        back_populates="character_data",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class UserCharacters(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    character_id: int = Field(foreign_key="characterdata.id", nullable=False)

    user: Optional[User] = Relationship(back_populates="user_characters")
    character_data: Optional[CharacterData] = Relationship(
        back_populates="user_characters"
    )


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    openai_response_id: Optional[str] = Field(default=None, index=True)
    thread_id: int = Field(foreign_key="thread.id", nullable=False, index=True)
    user_id: int = Field(nullable=False, foreign_key="user.id", index=True)
    profile_id: int = Field(
        nullable=False, foreign_key="characterprofile.id", index=True
    )
    created_at: float = Field(default_factory=time.time, nullable=False, index=True)
    role: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False)

    user: Optional[User] = Relationship(back_populates="messages")
    character: Optional[CharacterProfile] = Relationship(back_populates="messages")
    thread: Optional["Thread"] = Relationship(back_populates="messages")


class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    character_id: int = Field(
        foreign_key="characterprofile.id", nullable=False, index=True
    )
    created_at: float = Field(default_factory=time.time, nullable=False, index=True)

    user: Optional[User] = Relationship(back_populates="threads")
    character: Optional[CharacterProfile] = Relationship(back_populates="threads")
    messages: List["Message"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
