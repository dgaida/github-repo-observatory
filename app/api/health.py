from fastapi import APIRouter
from ..cache.ttl_cache import ttl_cache

router = APIRouter()

@router.get("/health")
async def health_check():
    """Check the health of the application.

    Returns:
        dict: Health status, version, and cache size.
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "cache_size": len(ttl_cache._cache)
    }
