import pytest
from unittest.mock import AsyncMock, patch
from app.api.repos import list_repos
from app.cache.ttl_cache import ttl_cache
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
        ttl_cache._cache.clear()
        query = RepoListQuery(username="user")
        repos = await list_repos(query=query)

        # Assertions
        assert len(repos) == 1
        repo = repos[0]
        assert repo.name == "test-repo"
        assert repo.metrics.build_status == BuildStatus.SUCCESS
        assert repo.metrics.coverage_percentage == 85.0
        assert repo.metrics.commit_count == 42

@pytest.mark.asyncio
async def test_repo_with_pages_pipeline():
    """Test that GitHub Pages URL is correctly fetched and included."""
    with patch("app.api.repos.github_client") as mock_client, \
         patch("app.api.repos.ActionsService") as mock_actions, \
         patch("app.api.repos.CoverageService") as mock_coverage, \
         patch("app.api.repos.QualityService") as mock_quality, \
         patch("app.api.repos.BadgeService") as mock_badges:

        # Mock GitHub API Responses
        mock_client.get_user_repos = AsyncMock(return_value=[{
            "name": "pages-repo",
            "full_name": "user/pages-repo",
            "html_url": "https://github.com/user/pages-repo",
            "description": "Pages repository",
            "owner": {"login": "user"},
            "has_pages": True
        }])
        mock_client.get_authenticated_user = AsyncMock(return_value={"login": "user"})
        mock_client.get_last_commit = AsyncMock(return_value=None)
        mock_client.get_commit_count = AsyncMock(return_value=10)
        mock_client.get_pages_url = AsyncMock(return_value="https://user.github.io/pages-repo/")

        # Mock Services
        mock_actions.get_build_status = AsyncMock(return_value=BuildStatus.SUCCESS)
        mock_coverage.get_coverage = AsyncMock(return_value=None)
        mock_quality.get_quality_tools = AsyncMock(return_value=[])
        mock_quality.get_codeql_status = AsyncMock(return_value="none")
        mock_badges.get_all_badges = AsyncMock(return_value=[])

        # Execute
        ttl_cache._cache.clear()
        query = RepoListQuery(username="user")
        repos = await list_repos(query=query)

        # Assertions
        assert len(repos) == 1
        repo = repos[0]
        assert repo.name == "pages-repo"
        assert str(repo.pages_url).rstrip("/") == "https://user.github.io/pages-repo"
        mock_client.get_pages_url.assert_called_once_with("user", "pages-repo")

@pytest.mark.asyncio
async def test_repo_with_empty_homepage_pipeline():
    """Test that empty homepage string is handled correctly (converted to None)."""
    with patch("app.api.repos.github_client") as mock_client, \
         patch("app.api.repos.ActionsService") as mock_actions, \
         patch("app.api.repos.CoverageService") as mock_coverage, \
         patch("app.api.repos.QualityService") as mock_quality, \
         patch("app.api.repos.BadgeService") as mock_badges:

        # Mock GitHub API Responses with empty homepage
        mock_client.get_user_repos = AsyncMock(return_value=[{
            "name": "empty-homepage-repo",
            "full_name": "user/empty-homepage-repo",
            "html_url": "https://github.com/user/empty-homepage-repo",
            "description": "Repo with empty homepage",
            "owner": {"login": "user"},
            "has_pages": False,
            "homepage": ""
        }])
        mock_client.get_authenticated_user = AsyncMock(return_value={"login": "user"})
        mock_client.get_last_commit = AsyncMock(return_value=None)
        mock_client.get_commit_count = AsyncMock(return_value=5)

        # Mock Services
        mock_actions.get_build_status = AsyncMock(return_value=BuildStatus.UNKNOWN)
        mock_coverage.get_coverage = AsyncMock(return_value=None)
        mock_quality.get_quality_tools = AsyncMock(return_value=[])
        mock_quality.get_codeql_status = AsyncMock(return_value="none")
        mock_badges.get_all_badges = AsyncMock(return_value=[])

        # Execute
        ttl_cache._cache.clear()
        query = RepoListQuery(username="user")
        # This used to raise ValidationError
        repos = await list_repos(query=query)

        # Assertions
        assert len(repos) == 1
        repo = repos[0]
        assert repo.name == "empty-homepage-repo"
        assert repo.pages_url is None
