import pytest
from app.exceptions import GitHubAPIError, GitHubRateLimitError, ResourceNotFoundError
from datetime import datetime

def test_github_api_error():
    err = GitHubAPIError("message", 500)
    assert err.status_code == 500
    assert str(err) == "message"

def test_github_rate_limit_error():
    reset = datetime.now()
    err = GitHubRateLimitError(reset_at=reset)
    assert err.status_code == 429
    assert err.reset_at == reset
    assert "rate limit" in str(err)

def test_resource_not_found_error():
    err = ResourceNotFoundError("Repo", "user/repo")
    assert err.status_code == 404
    assert err.resource_type == "Repo"
    assert err.identifier == "user/repo"
    assert "Repo 'user/repo' not found" in str(err)
