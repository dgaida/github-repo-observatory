import pytest
import time
from app.cache.ttl_cache import TTLCache

def test_ttl_cache_set_and_get():
    """Cache should store and retrieve values."""
    cache = TTLCache(default_ttl=60)
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"

def test_ttl_cache_expiry():
    """Cache entries should expire after TTL."""
    cache = TTLCache(default_ttl=1)  # 1 second
    cache.set("key1", "value1")
    time.sleep(1.1)
    assert cache.get("key1") is None

def test_ttl_cache_custom_ttl():
    """Custom TTL should override default_ttl."""
    cache = TTLCache(default_ttl=60)
    cache.set("short", "value", ttl=1)
    time.sleep(1.1)
    assert cache.get("short") is None

def test_ttl_cache_delete():
    """Cache should allow deleting entries."""
    cache = TTLCache()
    cache.set("key", "value")
    cache.delete("key")
    assert cache.get("key") is None
