import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client():
    """Synchronous-style async client for FastAPI testing."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")
