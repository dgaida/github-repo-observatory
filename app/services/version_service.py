from typing import Optional, List
from .badge_service import BadgeService
from .github_client import github_client
from ..parsers.shield_parser import ShieldParser

class VersionService:
    @staticmethod
    async def get_version(owner: str, repo: str, badges: Optional[List[str]] = None) -> Optional[str]:
        """
        Orchestrates version discovery for a repository.

        1. Try to extract from README badges.
        2. Fallback to latest GitHub release.
        3. Fallback to latest GitHub tag.
        """
        # 1. README badges
        if badges is None:
            badges = await BadgeService.get_all_badges(owner, repo)

        for url in badges:
            version = ShieldParser.extract_version(url)
            if version:
                # Clean up 'v' prefix if present for consistency
                return version.lstrip('v')

        # 2. Latest Release
        release = await github_client.get_latest_release(owner, repo)
        if release:
            return release.lstrip('v')

        # 3. Latest Tag
        tag = await github_client.get_latest_tag(owner, repo)
        if tag:
            return tag.lstrip('v')

        return None
