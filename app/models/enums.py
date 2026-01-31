from enum import Enum

class BuildStatus(str, Enum):
    """Build/CI status values."""
    SUCCESS = "success"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    UNKNOWN = "unknown"

class CodeQLStatus(str, Enum):
    """CodeQL analysis status."""
    ACTIVE = "active"
    FAILURE = "failure"
    NONE = "none"
    UNKNOWN = "unknown"

class FilterValue(str, Enum):
    """Filter query parameter values."""
    PASS = "pass"
    FAIL = "fail"
    NONE = "none"
