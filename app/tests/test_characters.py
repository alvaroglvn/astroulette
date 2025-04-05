import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_new_character():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=&quot;http://test&quot;
    ) as ac:
    
