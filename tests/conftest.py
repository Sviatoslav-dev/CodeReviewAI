import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from main import app


@pytest.fixture
def app_client():
    return TestClient(app)


@pytest.fixture(scope="function")
def redis_mock_client():
    with patch("repositories_cache.redis.Redis.from_url") as mock_redis_from_url:
        mock_redis_client = AsyncMock()
        mock_redis_from_url.return_value = mock_redis_client
        yield mock_redis_client
