from pydantic import BaseModel, Field, field_validator, BeforeValidator
from typing import Optional, Literal, Any, Annotated
from .enums import FilterValue

def empty_to_none(v: Any) -> Any:
    """Converts empty strings to None."""
    if v == "":
        return None
    return v

class RepoListQuery(BaseModel):
    """Query parameters for repository list.

    Attributes:
        username: GitHub username (optional).
        sort_by: Criteria to sort by.
        filter_test: Filter by test status.
        filter_quality: Filter by quality tools.
        filter_codeql: Filter by CodeQL status.
    """
    username: Annotated[Optional[str], BeforeValidator(empty_to_none)] = None
    sort_by: Annotated[Optional[Literal["coverage", "status", "last_commit"]], BeforeValidator(empty_to_none)] = None
    filter_test: Annotated[Optional[FilterValue], BeforeValidator(empty_to_none)] = None
    filter_quality: Annotated[Optional[FilterValue], BeforeValidator(empty_to_none)] = None
    filter_codeql: Annotated[Optional[FilterValue], BeforeValidator(empty_to_none)] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Validates GitHub username format."""
        if v is None:
            return v
        # GitHub usernames: alphanumeric, single hyphens, no start/end with hyphen, max 39 chars
        if not v.replace('-', '').isalnum():
            raise ValueError("Invalid GitHub username format")
        if len(v) > 39:
            raise ValueError("Username too long")
        return v
