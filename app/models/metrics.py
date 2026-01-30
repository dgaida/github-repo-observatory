from pydantic import BaseModel
from typing import Optional, List

class RepoMetrics(BaseModel):
    build_status: Optional[str] = "unknown"  # e.g., passing, failing, unknown
    failing_tests_count: Optional[int] = None
    coverage_percentage: Optional[float] = None
    codeql_status: Optional[str] = "unknown"  # e.g., active, failing, none
    quality_tools: List[str] = []  # e.g., ["SonarCloud", "Code Climate"]
    last_commit_at: Optional[str] = None
    commit_count: Optional[int] = None
    readme_badges: List[str] = []  # URLs of badges found in README
