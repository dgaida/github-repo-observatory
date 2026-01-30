import httpx
import re
from typing import List, Dict, Any, Optional
from ..config import config
from ..utils.rate_limit import github_rate_limiter
from ..utils.logging import logger

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

        if response.status_code == 403 and "rate limit exceeded" in response.text:
            logger.error("GitHub API rate limit exceeded")
            raise Exception("GitHub API rate limit exceeded")

        response.raise_for_status()
        return response.json()

    async def get_authenticated_user(self) -> Dict[str, Any]:
        """Fetch the authenticated user's profile."""
        return await self._get("user")

    async def get_user_repos(self, username: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch repositories for a user. If username is None, fetch for the authenticated user."""
        if username:
            return await self._get(f"users/{username}/repos")
        else:
            return await self._get("user/repos")

    async def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """Fetch the README content for a repository."""
        try:
            data = await self._get(f"repos/{owner}/{repo}/readme")
            # GitHub returns README content encoded in base64
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        except Exception as e:
            logger.warning(f"Could not fetch README for {owner}/{repo}: {e}")
            return None

    async def get_workflow_runs(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Fetch recent workflow runs for a repository."""
        try:
            data = await self._get(f"repos/{owner}/{repo}/actions/runs", params={"per_page": 5})
            return data.get("workflow_runs", [])
        except Exception as e:
            logger.warning(f"Could not fetch workflow runs for {owner}/{repo}: {e}")
            return []

    async def get_workflow_run_logs(self, owner: str, repo: str, run_id: int) -> Optional[str]:
        """Fetch logs for a workflow run (this usually returns a redirect to a zip)."""
        # Note: Parsing logs from the zip is complex.
        # For now, we'll return None or a placeholder.
        return None

    async def get_last_commit(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Fetch the latest commit for a repository."""
        try:
            commits = await self._get(f"repos/{owner}/{repo}/commits", params={"per_page": 1})
            return commits[0] if commits else None
        except Exception as e:
            logger.warning(f"Could not fetch last commit for {owner}/{repo}: {e}")
            return None

    async def get_commit_count(self, owner: str, repo: str) -> int:
        """Estimate commit count using the Link header from the commits endpoint."""
        try:
            await github_rate_limiter.wait()
            client = self.get_client()
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            response = await client.get(url, params={"per_page": 1})

            if response.status_code != 200:
                return 0

            if "Link" in response.headers:
                links = response.headers["Link"]
                # Example: <...page=2>; rel="next", <...page=123>; rel="last"
                match = re.search(r'page=(\d+)>; rel="last"', links)
                if match:
                    return int(match.group(1))

            # If no Link header, there's likely only 1 page
            return len(response.json())
        except Exception as e:
            logger.warning(f"Could not fetch commit count for {owner}/{repo}: {e}")
            return 0

github_client = GitHubClient()
