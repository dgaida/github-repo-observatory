import pytest
from unittest.mock import AsyncMock, patch
from app.api.repos import list_repos
from app.models.requests import RepoListQuery
from app.models.enums import BuildStatus

@pytest.mark.asyncio
async def test_full_repo_analysis_pipeline():
    """End-to-end test from GitHub API mocks to Repository object."""
    # We need to patch github_client in app.api.repos because it was imported there
    with patch("app.api.repos.github_client") as mock_client, \
         patch("app.api.repos.ActionsService") as mock_actions, \
         patch("app.api.repos.CoverageService") as mock_coverage, \
         patch("app.api.repos.QualityService") as mock_quality, \
         patch("app.api.repos.BadgeService") as mock_badges:

        # Mock GitHub API Responses for the client calls in repos.py
        mock_client.get_user_repos = AsyncMock(return_value=[{
            "name": "test-repo",
            "full_name": "user/test-repo",
            "html_url": "https://github.com/user/test-repo",
            "description": "Test repository",
            "owner": {"login": "user"}
        }])
        mock_client.get_authenticated_user = AsyncMock(
            return_value={"login": "user"}
        )
        mock_client.get_last_commit = AsyncMock(return_value={
            "commit": {"committer": {"date": "2024-01-15T10:00:00Z"}}
        })
        mock_client.get_commit_count = AsyncMock(return_value=42)

        # Mock Services
        mock_actions.get_build_status = AsyncMock(return_value=BuildStatus.SUCCESS)
        mock_coverage.get_coverage = AsyncMock(return_value=85.0)
        mock_quality.get_quality_tools = AsyncMock(return_value=["SonarCloud"])
        mock_quality.get_codeql_status = AsyncMock(return_value="active")
        mock_badges.get_all_badges = AsyncMock(return_value=["badge1"])

        # Execute
        query = RepoListQuery(username="user")
        repos = await list_repos(query=query)

        # Assertions
        assert len(repos) == 1
        repo = repos[0]
        assert repo.name == "test-repo"
        assert repo.metrics.build_status == BuildStatus.SUCCESS
        assert repo.metrics.coverage_percentage == 85.0
        assert repo.metrics.commit_count == 42
