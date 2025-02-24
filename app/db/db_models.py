from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(nullable=False, unique=True, index=True)
    email: str = Field(nullable=False, unique=True, index=True)

    character_data: List["CharacterData"] = Relationship(back_populates="user")
    thread: List["Thread"] = Relationship(back_populates="user", cascade_delete=True)
    user_characters: List["UserCharacters"] = Relationship(
        back_populates="user", cascade_delete=True
    )


class Assistant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    assistant_id: str = Field(nullable=False)
    created_at: int = Field(nullable=False, index=True)
    name: str = Field(nullable=False)
    model: str = Field(nullable=False, index=True)
    instructions: str = Field(nullable=False)
    temperature: float = Field(default=1, index=True)

    character_data: Optional["CharacterData"] = Relationship(back_populates="assistant")
    thread: List["Thread"] = Relationship(
        back_populates="assistant", cascade_delete=True
    )


class CharacterProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(nullable=False, index=True)
    planet_name: str = Field(nullable=False)
    planet_description: str = Field(nullable=False)
    personality_traits: str = Field(nullable=False)
    speech_style: str = Field(nullable=False)
    quirks: str = Field(nullable=False)

    character_data: Optional["CharacterData"] = Relationship(back_populates="profile")


class CharacterData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    image_prompt: str = Field(nullable=False)
    image_url: str = Field(nullable=False, default="PENDING")

    profile_id: int = Field(foreign_key="characterprofile.id", nullable=False)
    assistant_id: str = Field(foreign_key="assistant.id", nullable=False)
    generated_by: int = Field(foreign_key="user.id", nullable=False)

    profile: Optional[CharacterProfile] = Relationship(
        back_populates="character_data", cascade_delete=True
    )
    assistant: Optional[Assistant] = Relationship(
        back_populates="character_data", cascade_delete=True
    )
    user: Optional[User] = Relationship(back_populates="character_data")
    user_characters: List["UserCharacters"] = Relationship(
        back_populates="character_data", cascade_delete=True
    )


class UserCharacters(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", nullable=False)
    character_id: int = Field(foreign_key="characterdata.id", nullable=False)

    user: Optional[User] = Relationship(back_populates="user_characters")
    character_data: Optional[CharacterData] = Relationship(
        back_populates="user_characters"
    )


class Thread(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: int = Field(nullable=False, index=True)

    user_id: int = Field(nullable=False, foreign_key="user.id", index=True)
    character_id: int = Field(
        nullable=False, foreign_key="characterdata.id", index=True
    )
    assistant_id: str = Field(nullable=False, foreign_key="assistant.id")

    user: Optional[User] = Relationship(back_populates="thread")
    assistant: Optional[Assistant] = Relationship(back_populates="thread")
    messages: List["Message"] = Relationship(
        back_populates="thread", cascade_delete=True
    )


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    thread_id: int = Field(nullable=False, foreign_key="thread.id", index=True)
    created_at: int = Field(nullable=False, index=True)
    role: str = Field(nullable=False, index=True)
    content: str = Field(nullable=False)

    thread: Optional[Thread] = Relationship(back_populates="messages")
