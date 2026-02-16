from typing import Any

def empty_to_none(v: Any) -> Any:
    """Converts empty strings to None."""
    if v == "":
        return None
    return v
