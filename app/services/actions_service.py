from typing import List, Dict, Any, Optional
from .github_client import github_client
from ..models.enums import BuildStatus
from ..utils.logging import logger

class ActionsService:
    @staticmethod
    async def get_build_status(owner: str, repo: str) -> BuildStatus:
        """Determines the build status of the last workflow run.

        Args:
            owner: Repository owner.
            repo: Repository name.

        Returns:
            BuildStatus enum value.
        """
        runs = await github_client.get_workflow_runs(owner, repo)
        if not runs:
            return BuildStatus.UNKNOWN

        latest_run = runs[0]
        status = latest_run.get("status")
        conclusion = latest_run.get("conclusion")

        if status == "completed":
            if conclusion == "success":
                return BuildStatus.SUCCESS
            elif conclusion == "failure":
                return BuildStatus.FAILURE
            else:
                return BuildStatus.UNKNOWN
        elif status == "in_progress":
            return BuildStatus.IN_PROGRESS

        return BuildStatus.UNKNOWN

    @staticmethod
    async def get_failed_tests_count(owner: str, repo: str) -> Optional[int]:
        """Fetches the number of failed tests (placeholder)."""
        # Log parsing is currently not implemented due to API complexity.
        return None
