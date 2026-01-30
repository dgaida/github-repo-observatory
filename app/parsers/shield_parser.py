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

        # Codecov via Shields: /codecov/c/github/<USER>/<REPO>
        if "/codecov/c/" in url:
            return {
                "label": "coverage",
                "type": "codecov"
            }

        return None

    @staticmethod
    def extract_coverage(url: str) -> Optional[float]:
        """Extracts coverage percentage from a badge URL."""
        data = ShieldParser.parse_badge_url(url)
        if not data:
            return None

        if "coverage" in data.get("label", "").lower():
            if "message" in data:
                msg = data["message"]
                match = re.search(r'(\d+(?:\.\d+)?)', msg)
                if match:
                    return float(match.group(1))

            # If it's a dynamic badge (like Codecov via Shields), we might not have the message
            # in the URL itself. This would require fetching the badge or using dynamic extraction.
            # For now, we only support static badges or badges with the value in the URL.

        return None
