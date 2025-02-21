from sqlalchemy import Column, Integer, Float, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    active = Column(Boolean, default=True, index=True)

    character_data = relationship(
        "CharacterData",
        back_populates="user",
    )
    thread = relationship(
        "Thread",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    user_characters = relationship(
        "UserCharacters",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Assistant(Base):
    __tablename__ = "assistant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    created_at = Column(BigInteger, nullable=False, index=True)
    instructions = Column(String, nullable=False)
    model = Column(String, nullable=False, index=True)
    temperature = Column(Float, default=1, index=True)

    character_data = relationship("CharacterData", back_populates="assistant")
    thread = relationship(
        "Thread",
        back_populates="assistant",
        cascade="all",
        passive_deletes=True,
    )


class CharacterProfile(Base):
    __tablename__ = "character_profile"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    planet_name = Column(String, nullable=False, index=True)
    planet_description = Column(String, nullable=False)
    personality_traits = Column(String, nullable=False)
    speech_style = Column(String, nullable=False)
    quirks = Column(String, nullable=False)

    character_data = relationship("CharacterData", back_populates="character_profile")


class CharacterData(Base):
    __tablename__ = "character_data"

    id = Column(Integer, primary_key=True, index=True)
    image_prompt = Column(String, nullable=False)
    image_url = Column(String, nullable=False, default="PENDING")
    profile_id = Column(
        Integer, ForeignKey("character_profile.id", ondelete="CASCADE"), nullable=False
    )
    assistant_id = Column(
        Integer, ForeignKey("assistant.id", ondelete="CASCADE"), nullable=False
    )
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    character_profile = relationship(
        "CharacterProfile",
        back_populates="character_data",
        passive_deletes=True,
    )
    assistant = relationship(
        "Assistant",
        back_populates="character_data",
        passive_deletes=True,
    )
    user = relationship("User", back_populates="character_data")
    user_characters = relationship(
        "UserCharacters",
        back_populates="character_data",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    threads = relationship(
        "Thread",
        back_populates="character_data",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class UserCharacters(Base):
    __tablename__ = "user_characters"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    character_id = Column(
        Integer,
        ForeignKey("character_data.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )

    character_data = relationship(
        "CharacterData",
        back_populates="user_characters",
    )
    user = relationship(
        "User",
        back_populates="user_characters",
    )


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(
        Integer, ForeignKey("thread.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(BigInteger, nullable=False, index=True)
    role = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)

    thread = relationship("Thread", back_populates="messages")


class Thread(Base):
    __tablename__ = "thread"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(BigInteger, nullable=False, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    character_id = Column(
        Integer, ForeignKey("character_data.id", ondelete="CASCADE"), nullable=False
    )
    assistant_id = Column(
        Integer, ForeignKey("assistant.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="thread", passive_deletes=True)
    assistant = relationship("Assistant", back_populates="thread", passive_deletes=True)
    character_data = relationship(
        "CharacterData", back_populates="threads", passive_deletes=True
    )
    messages = relationship(
        "Message",
        back_populates="thread",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
