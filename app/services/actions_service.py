from typing import List, Dict, Any, Optional
from .github_client import github_client
from ..parsers.action_logs import ActionLogsParser

class ActionsService:
    @staticmethod
    async def get_build_status(owner: str, repo: str) -> str:
        runs = await github_client.get_workflow_runs(owner, repo)
        if not runs:
            return "unknown"

        latest_run = runs[0]
        status = latest_run.get("status")
        conclusion = latest_run.get("conclusion")

        if status == "completed":
            return conclusion if conclusion else "unknown"
        return "in_progress"

    @staticmethod
    async def get_failed_tests_count(owner: str, repo: str) -> Optional[int]:
        # Log parsing is hard due to GitHub API returning zip files for logs.
        # This is a placeholder for now.
        return None
