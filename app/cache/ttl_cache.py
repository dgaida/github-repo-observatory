import time
from typing import Any, Dict, Optional, Tuple

class TTLCache:
    def __init__(self, default_ttl: int = 3600):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expiry = time.time() + (ttl or self.default_ttl)
        self._cache[key] = (value, expiry)

    def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]

ttl_cache = TTLCache()
