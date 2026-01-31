import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional
from .logging import logger

class RateLimiter:
    """Rate Limiter with basic interval-based limiting."""
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

class AdaptiveRateLimiter:
    """Rate Limiter with exponential backoff and adaptive interval."""

    def __init__(self, requests_per_hour: int = 5000):
        self.interval = 3600 / requests_per_hour
        self.last_request_time = 0.0
        self.backoff_until: Optional[datetime] = None
        self.consecutive_errors = 0

    async def wait(self):
        """Wait if necessary, adapting to errors."""
        # Check if in backoff period
        if self.backoff_until:
            now = datetime.now()
            if now < self.backoff_until:
                wait_seconds = (self.backoff_until - now).total_seconds()
                logger.warning(f"Rate limit backoff: waiting {wait_seconds:.2f}s")
                await asyncio.sleep(wait_seconds)
            else:
                self.backoff_until = None
                self.consecutive_errors = 0

        # Normal rate limiting
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.interval:
            wait_time = self.interval - elapsed
            await asyncio.sleep(wait_time)
        self.last_request_time = time.time()

    def trigger_backoff(self):
        """Activate exponential backoff after a rate limit error."""
        self.consecutive_errors += 1
        # Backoff: 60s, 120s, 240s, max 300s
        backoff_seconds = min(300, 60 * (2 ** (self.consecutive_errors - 1)))
        self.backoff_until = datetime.now() + timedelta(seconds=backoff_seconds)
        logger.error(f"Rate limit hit. Backing off for {backoff_seconds}s")

# Default rate limiter for GitHub API
github_rate_limiter = AdaptiveRateLimiter(requests_per_hour=5000)
