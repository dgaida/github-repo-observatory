from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from .enums import BuildStatus, CodeQLStatus

class RepoMetrics(BaseModel):
    """Metrics for a repository.

    Attributes:
        build_status: Status of the last CI run.
        failing_tests_count: Number of failing tests (0-N).
        coverage_percentage: Test coverage in percent (0-100).
        codeql_status: Status of CodeQL analysis.
        quality_tools: List of detected quality tools.
        last_commit_at: ISO 8601 timestamp of the last commit.
        commit_count: Total number of commits.
        readme_badges: URLs of badge images found in README.
    """
    build_status: BuildStatus = BuildStatus.UNKNOWN
    failing_tests_count: Optional[int] = Field(None, ge=0)
    coverage_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    codeql_status: CodeQLStatus = CodeQLStatus.NONE
    quality_tools: List[str] = Field(default_factory=list)
    last_commit_at: Optional[str] = None
    commit_count: Optional[int] = Field(None, ge=0)
    readme_badges: List[str] = Field(default_factory=list)

    @field_validator('last_commit_at')
    @classmethod
    def validate_timestamp(cls, v: Optional[str]) -> Optional[str]:
        """Validates ISO 8601 timestamp format (basic check)."""
        if v is None:
            return v
        # Basic check: should at least look like a date
        if len(v) < 10:
            raise ValueError("Invalid timestamp format")
        return v
