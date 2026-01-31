from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from .enums import FilterValue

class RepoListQuery(BaseModel):
    """Query parameters for repository list.

    Attributes:
        username: GitHub username (optional).
        sort_by: Criteria to sort by.
        filter_test: Filter by test status.
        filter_quality: Filter by quality tools.
        filter_codeql: Filter by CodeQL status.
    """
    username: Optional[str] = None
    sort_by: Optional[Literal["coverage", "status", "last_commit"]] = None
    filter_test: Optional[FilterValue] = None
    filter_quality: Optional[FilterValue] = None
    filter_codeql: Optional[FilterValue] = None

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
