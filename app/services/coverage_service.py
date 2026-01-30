from typing import Optional
from .badge_service import BadgeService
from ..parsers.shield_parser import ShieldParser

class CoverageService:
    @staticmethod
    async def get_coverage(owner: str, repo: str) -> Optional[float]:
        badges = await BadgeService.get_all_badges(owner, repo)
        for badge_url in badges:
            coverage = ShieldParser.extract_coverage(badge_url)
            if coverage is not None:
                return coverage
        return None
