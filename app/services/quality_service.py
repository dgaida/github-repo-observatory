from typing import List
from .badge_service import BadgeService

class QualityService:
    @staticmethod
    async def get_quality_tools(owner: str, repo: str) -> List[str]:
        badges = await BadgeService.get_all_badges(owner, repo)
        tools = []

        for url in badges:
            url_lower = url.lower()
            if "sonarcloud" in url_lower or "sonar" in url_lower:
                if "SonarCloud" not in tools:
                    tools.append("SonarCloud")
            if "codeclimate" in url_lower:
                if "Code Climate" not in tools:
                    tools.append("Code Climate")
            if "codeql" in url_lower:
                if "CodeQL" not in tools:
                    tools.append("CodeQL")
            if "codecov" in url_lower:
                if "Codecov" not in tools:
                    tools.append("Codecov")

        return tools

    @staticmethod
    async def get_codeql_status(owner: str, repo: str) -> str:
        # Check if CodeQL workflow exists
        # This is a simplified check
        tools = await QualityService.get_quality_tools(owner, repo)
        return "active" if "CodeQL" in tools else "none"
