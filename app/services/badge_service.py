from typing import List
from ..parsers.readme_parser import ReadmeParser
from .github_client import github_client

class BadgeService:
    @staticmethod
    async def get_all_badges(owner: str, repo: str) -> List[str]:
        readme = await github_client.get_readme(owner, repo)
        if not readme:
            return []
        return ReadmeParser.extract_badges(readme)
