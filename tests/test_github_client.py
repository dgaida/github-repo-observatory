import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.github_client import GitHubClient

@pytest.mark.asyncio
async def test_get_commit_count():
    client = GitHubClient()
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Link": '<...page=123>; rel="last"'}
        mock_get.return_value = mock_response

        count = await client.get_commit_count("owner", "repo")
        assert count == 123

@pytest.mark.asyncio
async def test_get_last_commit():
    client = GitHubClient()
    with patch.object(client, "_get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = [{"commit": {"committer": {"date": "2024-01-01T00:00:00Z"}}}]

        commit = await client.get_last_commit("owner", "repo")
        assert commit["commit"]["committer"]["date"] == "2024-01-01T00:00:00Z"
