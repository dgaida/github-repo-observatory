import re
from typing import Optional, Dict

class ShieldParser:
    @staticmethod
    def parse_badge_url(url: str) -> Optional[Dict[str, str]]:
        """
        Parses a Shields.io URL to extract label and message.
        Example: https://img.shields.io/badge/coverage-80%25-green
        """
        if "img.shields.io" not in url:
            return None

        # Static badge: /badge/<LABEL>-<MESSAGE>-<COLOR>
        static_match = re.search(r'/badge/([^/]+)-([^/]+)-([^/]+)', url)
        if static_match:
            return {
                "label": static_match.group(1).replace('_', ' '),
                "message": static_match.group(2).replace('_', ' ').replace('%25', '%'),
                "color": static_match.group(3)
            }

        # Workflow status: /github/actions/workflow/status/<USER>/<REPO>/<WORKFLOW>.svg
        if "/github/actions/workflow/status/" in url:
            return {
                "label": "build",
                "type": "workflow_status"
            }

        return None

    @staticmethod
    def extract_coverage(url: str) -> Optional[float]:
        """Extracts coverage percentage from a badge URL."""
        data = ShieldParser.parse_badge_url(url)
        if data and "coverage" in data["label"].lower():
            msg = data["message"]
            match = re.search(r'(\d+(?:\.\d+)?)', msg)
            if match:
                return float(match.group(1))
        return None
