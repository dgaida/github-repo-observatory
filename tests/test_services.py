import pytest
from unittest.mock import AsyncMock, patch
from app.services.actions_service import ActionsService
from app.services.coverage_service import CoverageService
from app.services.quality_service import QualityService

@pytest.mark.asyncio
async def test_get_build_status():
    with patch("app.services.actions_service.github_client") as mock_client:
        mock_client.get_workflow_runs = AsyncMock(return_value=[
            {"status": "completed", "conclusion": "success"}
        ])
        status = await ActionsService.get_build_status("owner", "repo")
        assert status == "success"

@pytest.mark.asyncio
async def test_get_coverage():
    with patch("app.services.coverage_service.BadgeService.get_all_badges") as mock_badges:
        mock_badges.return_value = ["https://img.shields.io/badge/coverage-90%25-green"]
        coverage = await CoverageService.get_coverage("owner", "repo")
        assert coverage == 90.0

@pytest.mark.asyncio
async def test_get_quality_tools():
    with patch("app.services.quality_service.BadgeService.get_all_badges") as mock_badges:
        mock_badges.return_value = [
            "https://img.shields.io/badge/sonarcloud-passed-blue",
            "https://img.shields.io/badge/codeql-active-green",
            "https://img.shields.io/codecov/c/github/user/repo"
        ]
        tools = await QualityService.get_quality_tools("owner", "repo")
        assert "SonarCloud" in tools
        assert "CodeQL" in tools
        assert "Codecov" in tools
