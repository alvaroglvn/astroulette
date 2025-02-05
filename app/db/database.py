from typing import List, Optional, Iterator

from fastapi import Depends, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


# Tables structure


class CharacterProfile(SQLModel, table=True):
    profile_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    planet_name: str = Field(nullable=False)
    planet_description: str = Field(nullable=False)
    personality_traits: str = Field(nullable=False)
    speech_style: str = Field(nullable=False)
    quirks: str = Field(nullable=False)

    users: List["UserCharacter"] = Relationship(back_populates="character")
    chats: List["Chat"] = Relationship(back_populates="character")


class CharacterData(SQLModel, table=True):
    character_id: Optional[int] = Field(default=None, primary_key=True)
    image_prompt: str = Field(nullable=False)
    image_url: str = Field(nullable=False)
    character_profile_id: int = Field(
        nullable=False, foreign_key="characterprofile.profile_id"
    )


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)

    characters: List["UserCharacter"] = Relationship(back_populates="user")
    chats: List["Chat"] = Relationship(back_populates="user")


class UserCharacter(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    character_id: int = Field(
        foreign_key="characterprofile.profile_id", primary_key=True
    )

    user: User = Relationship(back_populates="characters")
    character: CharacterProfile = Relationship(back_populates="users")


class Chat(SQLModel, table=True):
    chat_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="user.user_id")
    character_id: int = Field(nullable=False, foreign_key="characterprofile.profile_id")
    user_message: str = Field(nullable=False)
    ai_response: str = Field(nullable=False)

    user: User = Relationship(back_populates="chats")
    character: CharacterProfile = Relationship(back_populates="chats")


# Engine
sqlite_file_name = "app/db/alien_talk.db"
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
