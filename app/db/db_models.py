from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
import time


class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    image_prompt: str = Field(nullable=False)
    image_url: str = Field(default="PENDING")
    generated_by: int = Field(foreign_key="user.id")
    name: str = Field(nullable=False, index=True)
    planet_name: str = Field(nullable=False)
    planet_description: str = Field(nullable=False)
    personality_traits: str = Field(nullable=False)
    speech_style: str = Field(nullable=False)
    quirks: str = Field(nullable=False)
    human_relationship: str = Field(nullable=False)

    threads: List["Thread"] = Relationship(
        back_populates="character",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    messages: List["Message"] = Relationship(
        back_populates="character",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(nullable=False, unique=True, index=True)
    email: EmailStr = Field(nullable=False, index=True)
    role: str = Field(nullable=False, default="user", index=True)
    status: str = Field(nullable=False, default="active", index=True)
    login_token: str = Field(nullable=True, default=None, index=True)
    token_expiry: int = Field(nullable=True, default=None, index=True)

    messages: List["Message"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    threads: List["Thread"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    openai_response_id: Optional[str] = Field(default=None, index=True)
    thread_id: int = Field(foreign_key="thread.id", nullable=False, index=True)
    user_id: int = Field(nullable=False, foreign_key="user.id", index=True)
    profile_id: int = Field(
        nullable=False,
        foreign_key="character.id",
        index=True,
    )
    created_at: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False)

    user: Optional[User] = Relationship(back_populates="messages")
    character: Optional[Character] = Relationship(back_populates="messages")
    thread: Optional["Thread"] = Relationship(back_populates="messages")


class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    character_id: int = Field(foreign_key="character.id", nullable=False, index=True)
    created_at: int = Field(nullable=False, index=True)

    user: Optional[User] = Relationship(back_populates="threads")
    character: Optional[Character] = Relationship(back_populates="threads")
    messages: List["Message"] = Relationship(
        back_populates="thread",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
