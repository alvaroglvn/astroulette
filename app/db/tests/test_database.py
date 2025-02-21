import pytest
from sqlalchemy.orm import Session
from app.db.database_models import *


@pytest.fixture()
def mock_user(session: Session) -> User:
    user = User(username="TestUser", email="test@test.com", active=True)
    session.add(user)
    session.commit()
    return user
