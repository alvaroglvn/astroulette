# import pytest
# from typing import AsyncGenerator
# from sqlmodel.ext.asyncio import AsyncSession
# from sqlmodel import SQLModel
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
# from sqlalchemy.orm import sessionmaker
# from sqlmodel.pool import StaticPool
# from app.db.db_models import Character, User


# @pytest.fixture(name="session")
# async def async_session_fixture() -> AsyncGenerator[AsyncSession, None]:
#     engine: AsyncEngine = create_async_engine(
#         "sqlite+aiosqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

#     async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

#     async with async_session() as session:
#         yield session


# @pytest.fixture(name="mock_user")
# def mock_user() -> User:
#     return User(
#         username="John Carter",
#         email="john@barsoom.com",
#         role="user",
#         status="active",
#         login_token="token123",
#         token_expiry=1699999999,
#     )
