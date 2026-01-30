import asyncio
from fastapi import APIRouter, Query
from typing import List, Optional
from ..models.repo import Repository
from ..models.metrics import RepoMetrics
from ..services.github_client import github_client
from ..services.actions_service import ActionsService
from ..services.coverage_service import CoverageService
from ..services.quality_service import QualityService
from ..cache.ttl_cache import ttl_cache

router = APIRouter()

async def fetch_repo_metrics(repo_dict):
    owner = repo_dict["owner"]["login"]
    name = repo_dict["name"]

    # Fetch metrics in parallel for each repo
    build_status_task = ActionsService.get_build_status(owner, name)
    coverage_task = CoverageService.get_coverage(owner, name)
    quality_tools_task = QualityService.get_quality_tools(owner, name)
    codeql_status_task = QualityService.get_codeql_status(owner, name)

    build_status, coverage, quality_tools, codeql_status = await asyncio.gather(
        build_status_task, coverage_task, quality_tools_task, codeql_status_task
    )

    metrics = RepoMetrics(
        build_status=build_status,
        coverage_percentage=coverage,
        quality_tools=quality_tools,
        codeql_status=codeql_status
    )

    return Repository(
        name=name,
        full_name=repo_dict["full_name"],
        html_url=repo_dict["html_url"],
        description=repo_dict.get("description"),
        metrics=metrics
    )

@router.get("/repos", response_model=List[Repository])
async def list_repos(username: Optional[str] = Query(None)):
    cache_key = f"repos_{username or 'authed'}"
    cached_data = ttl_cache.get(cache_key)
    if cached_data:
        return cached_data

    try:
        repos_data = await github_client.get_user_repos(username)
    except Exception:
        return []

    # Process all repositories in parallel (with rate limiting handled in services)
    repositories = await asyncio.gather(*[fetch_repo_metrics(r) for r in repos_data])

    ttl_cache.set(cache_key, repositories)
    return repositories
