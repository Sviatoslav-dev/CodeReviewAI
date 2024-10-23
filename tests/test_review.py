import pytest


@pytest.mark.asyncio
async def test_review_positive(redis_mock_client, app_client):
    redis_mock_client.get.return_value = None
    redis_mock_client.setex.return_value = None

    data = {
        "assignment_description": "This is echo server with asyncio",
        "github_repo_url": "https://github.com/Sviatoslav-dev/asyncio_echo_server",
        "candidate_level": "junior"
    }

    response = app_client.post("/review", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_cache(redis_mock_client, app_client):
    redis_mock_client.get.return_value = '{"found_files": "files_list", ' \
                                         '"review_result": "some feedback"}'
    redis_mock_client.setex.return_value = None

    data = {
        "assignment_description": "This is echo server with asyncio",
        "github_repo_url": "https://github.com/Sviatoslav-dev/asyncio_echo_server",
        "candidate_level": "junior"
    }

    response = app_client.post("/review", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_not_exist_repo(app_client):
    data = {
        "assignment_description": "This is echo server with asyncio",
        "github_repo_url": "https://github.com/Sviatoslav-dev/not_exist_repo",
        "candidate_level": "junior"
    }

    response = app_client.post("/review", json=data)
    assert response.status_code == 404
