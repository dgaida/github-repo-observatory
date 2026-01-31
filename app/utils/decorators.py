from functools import wraps
from typing import TypeVar, Optional, Callable, Any
from .logging import logger
from httpx import HTTPStatusError, RequestError

T = TypeVar('T')

def handle_github_api_errors(
    default_return: T,
    log_level: str = "warning"
) -> Callable:
    """Decorator for handling GitHub API errors.

    Args:
        default_return: Value to return if an error occurs.
        log_level: Logging level for the error ('debug', 'warning', 'error').
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.debug(f"{func.__name__}: Resource not found")
                else:
                    log_func = getattr(logger, log_level)
                    log_func(f"{func.__name__}: HTTP {e.response.status_code} - {e}")
                return default_return
            except (RequestError, ValueError) as e:
                log_func = getattr(logger, log_level)
                log_func(f"{func.__name__}: {type(e).__name__}: {e}")
                return default_return
            except Exception as e:
                log_func = getattr(logger, log_level)
                log_func(f"{func.__name__}: Unexpected error: {type(e).__name__}: {e}")
                return default_return
        return wrapper
    return decorator
