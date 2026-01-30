import asyncio
import time
from .logging import logger

class RateLimiter:
    def __init__(self, requests_per_hour: int = 5000):
        self.interval = 3600 / requests_per_hour
        self.last_request_time = 0.0

    async def wait(self):
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.interval:
            wait_time = self.interval - elapsed
            logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
            await asyncio.sleep(wait_time)
        self.last_request_time = time.time()

# Default rate limiter for GitHub API (unauthenticated is 60/hr, authenticated is 5000/hr)
github_rate_limiter = RateLimiter(requests_per_hour=5000)
