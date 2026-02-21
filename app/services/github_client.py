import base64
import httpx
import re
from typing import List, Dict, Any, Optional
from ..config import config
from ..utils.rate_limit import github_rate_limiter
from ..utils.logging import logger
from ..utils.decorators import handle_github_api_errors
from ..models.github_types import GitHubUser, WorkflowRun, CommitInfo, RepositoryData

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-repo-observatory"
        }
        if config.GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {config.GITHUB_TOKEN}"
        self._client = None

    def get_client(self):
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(headers=self.headers, timeout=30.0)
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        await github_rate_limiter.wait()
        client = self.get_client()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await client.get(url, params=params)

        if response.status_code == 403 and "rate limit exceeded" in response.text.lower():
            logger.error(f"GitHub API rate limit exceeded: {response.text}")
            github_rate_limiter.trigger_backoff()
            response.raise_for_status()

        response.raise_for_status()
        return response.json()

    @handle_github_api_errors(default_return={})
    async def get_authenticated_user(self) -> GitHubUser:
        """Fetch the authenticated user's profile."""
        return await self._get("user")

    @handle_github_api_errors(default_return=[])
    async def get_user_repos(self, username: Optional[str] = None) -> List[RepositoryData]:
        """Fetch repositories for a user. If username is None, fetch for the authenticated user."""
        if username:
            return await self._get(f"users/{username}/repos")
        else:
            return await self._get("user/repos")

    @handle_github_api_errors(default_return=None)
    async def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Fetch the README content for a repository.

        Returns:
            README content as string, or None if not found/accessible
        """
        data = await self._get(f"repos/{owner}/{repo}/readme")
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content

    @handle_github_api_errors(default_return=[])
    async def get_workflow_runs(self, owner: str, repo: str) -> List[WorkflowRun]:
        """Fetch recent workflow runs for a repository."""
        data = await self._get(f"repos/{owner}/{repo}/actions/runs", params={"per_page": 5})
        return data.get("workflow_runs", [])

    async def get_workflow_run_logs(self, owner: str, repo: str, run_id: int) -> Optional[str]:
        """Fetch logs for a workflow run."""
        # Note: Parsing logs from the zip is complex.
        return None

    @handle_github_api_errors(default_return=None)
    async def get_last_commit(self, owner: str, repo: str) -> Optional[CommitInfo]:
        """Fetch the latest commit for a repository."""
        commits = await self._get(f"repos/{owner}/{repo}/commits", params={"per_page": 1})
        return commits[0] if commits else None

    @handle_github_api_errors(default_return=0)
    async def get_commit_count(self, owner: str, repo: str) -> int:
        """Estimate commit count using the Link header from the commits endpoint."""
        # Note: _get already does wait(), but here we use client.get directly for Link header
        await github_rate_limiter.wait()
        client = self.get_client()
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        response = await client.get(url, params={"per_page": 1})

        if response.status_code == 403 and "rate limit exceeded" in response.text.lower():
            github_rate_limiter.trigger_backoff()
            response.raise_for_status()

        if response.status_code != 200:
            return 0

        if "Link" in response.headers:
            links = response.headers["Link"]
            match = re.search(r'page=(\d+)>; rel="last"', links)
            if match:
                return int(match.group(1))

        return len(response.json())

    @handle_github_api_errors(default_return=None)
    async def get_pages_url(self, owner: str, repo: str) -> Optional[str]:
        """Fetch the GitHub Pages URL for a repository.

        Returns:
            The GitHub Pages URL as a string, or None if not found/accessible.
        """
        data = await self._get(f"repos/{owner}/{repo}/pages")
        return data.get("html_url")

    @handle_github_api_errors(default_return=None)
    async def get_latest_release(self, owner: str, repo: str) -> Optional[str]:
        """Fetch the latest release for a repository."""
        data = await self._get(f"repos/{owner}/{repo}/releases/latest")
        return data.get("tag_name")

    @handle_github_api_errors(default_return=None)
    async def get_latest_tag(self, owner: str, repo: str) -> Optional[str]:
        """Fetch the latest tag for a repository."""
        tags = await self._get(f"repos/{owner}/{repo}/tags", params={"per_page": 1})
        return tags[0]["name"] if tags else None

github_client = GitHubClient()
