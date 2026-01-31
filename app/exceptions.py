from typing import Optional
from datetime import datetime

class GitHubObservatoryError(Exception):
    """Base exception for all errors in the application."""
    pass

class GitHubAPIError(GitHubObservatoryError):
    """Error communicating with the GitHub API."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)

class GitHubRateLimitError(GitHubAPIError):
    """GitHub API rate limit exceeded."""
    def __init__(self, reset_at: Optional[datetime] = None):
        self.reset_at = reset_at
        super().__init__("GitHub API rate limit exceeded", 429)

class ResourceNotFoundError(GitHubAPIError):
    """The requested resource was not found."""
    def __init__(self, resource_type: str, identifier: str):
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(f"{resource_type} '{identifier}' not found", 404)

class CacheError(GitHubObservatoryError):
    """Error in the caching system."""
    pass
