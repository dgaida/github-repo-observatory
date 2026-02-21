import pytest
from unittest.mock import AsyncMock, patch
from app.services.version_service import VersionService

@pytest.mark.asyncio
async def test_get_version_from_badge():
    with patch("app.services.version_service.BadgeService.get_all_badges") as mock_badges:
        mock_badges.return_value = ["https://img.shields.io/badge/version-1.5.0-blue"]

        version = await VersionService.get_version("owner", "repo")
        assert version == "1.5.0"

@pytest.mark.asyncio
async def test_get_version_fallback_to_release():
    with patch("app.services.version_service.BadgeService.get_all_badges") as mock_badges, \
         patch("app.services.version_service.github_client") as mock_client:

        mock_badges.return_value = []
        mock_client.get_latest_release = AsyncMock(return_value="v2.0.0")

        version = await VersionService.get_version("owner", "repo")
        assert version == "2.0.0"

@pytest.mark.asyncio
async def test_get_version_fallback_to_tag():
    with patch("app.services.version_service.BadgeService.get_all_badges") as mock_badges, \
         patch("app.services.version_service.github_client") as mock_client:

        mock_badges.return_value = []
        mock_client.get_latest_release = AsyncMock(return_value=None)
        mock_client.get_latest_tag = AsyncMock(return_value="v1.0.1-rc")

        version = await VersionService.get_version("owner", "repo")
        assert version == "1.0.1-rc"

@pytest.mark.asyncio
async def test_get_version_none():
    with patch("app.services.version_service.BadgeService.get_all_badges") as mock_badges, \
         patch("app.services.version_service.github_client") as mock_client:

        mock_badges.return_value = []
        mock_client.get_latest_release = AsyncMock(return_value=None)
        mock_client.get_latest_tag = AsyncMock(return_value=None)

        version = await VersionService.get_version("owner", "repo")
        assert version is None
