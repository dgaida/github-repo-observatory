from pydantic import BaseModel, HttpUrl
from typing import Optional
from .metrics import RepoMetrics

class Repository(BaseModel):
    name: str
    full_name: str
    html_url: HttpUrl
    pages_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    metrics: Optional[RepoMetrics] = None
