from typing import TypedDict, Literal, List, Optional, Any

class GitHubUser(TypedDict):
    """GitHub User API response."""
    login: str
    id: int
    avatar_url: str
    html_url: str

class WorkflowRun(TypedDict):
    """GitHub Workflow Run API response."""
    id: int
    status: Literal["queued", "in_progress", "completed", "waiting", "requested", "pending"]
    conclusion: Optional[Literal["success", "failure", "cancelled", "skipped", "timed_out", "action_required", "neutral"]]
    html_url: str
    created_at: str
    updated_at: str

class CommitInfo(TypedDict):
    """GitHub Commit API response."""
    sha: str
    commit: dict
    html_url: str
    url: str

class RepositoryData(TypedDict):
    """GitHub Repository API response."""
    name: str
    full_name: str
    html_url: str
    description: Optional[str]
    owner: GitHubUser
