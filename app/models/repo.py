from pydantic import BaseModel, HttpUrl, BeforeValidator
from typing import Optional, Annotated
from .metrics import RepoMetrics
from .validators import empty_to_none

class Repository(BaseModel):
    name: str
    full_name: str
    html_url: HttpUrl
    pages_url: Annotated[Optional[HttpUrl], BeforeValidator(empty_to_none)] = None
    description: Optional[str] = None
    metrics: Optional[RepoMetrics] = None
