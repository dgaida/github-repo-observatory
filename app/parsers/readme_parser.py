import re
from typing import List

class ReadmeParser:
    @staticmethod
    def extract_badges(content: str) -> List[str]:
        """
        Extracts image URLs that likely represent badges from markdown content.
        Looks for patterns like [![alt](badge_url)](link) or <img src="badge_url">
        """
        # Markdown image pattern: ![alt](url)
        md_images = re.findall(r'!\[.*?\]\((.*?)\)', content)

        # HTML image pattern: <img src="url">
        html_images = re.findall(r'<img [^>]*src="([^"]+)"', content)

        return list(set(md_images + html_images))
