import asyncio
from fastapi import APIRouter, Depends
from typing import List, Optional, Dict, Any
from ..models.repo import Repository
from ..models.metrics import RepoMetrics
from ..models.requests import RepoListQuery
from ..models.enums import BuildStatus, CodeQLStatus, FilterValue
from ..services.github_client import github_client
from ..services.actions_service import ActionsService
from ..services.coverage_service import CoverageService
from ..services.quality_service import QualityService
from ..services.badge_service import BadgeService
from ..cache.ttl_cache import ttl_cache

router = APIRouter()

async def fetch_repo_metrics(repo_dict: Dict[str, Any]) -> Repository:
    """Enriches a repository with metrics."""
    owner = repo_dict["owner"]["login"]
    name = repo_dict["name"]

    # Fetch metrics in parallel
    (build_status, coverage, quality_tools, codeql_status,
     badges, last_commit, commit_count) = await asyncio.gather(
        ActionsService.get_build_status(owner, name),
        CoverageService.get_coverage(owner, name),
        QualityService.get_quality_tools(owner, name),
        QualityService.get_codeql_status(owner, name),
        BadgeService.get_all_badges(owner, name),
        github_client.get_last_commit(owner, name),
        github_client.get_commit_count(owner, name)
    )

    last_commit_at = None
    if last_commit and "commit" in last_commit:
        last_commit_at = last_commit["commit"]["committer"]["date"]

    metrics = RepoMetrics(
        build_status=build_status,
        coverage_percentage=coverage,
        quality_tools=quality_tools,
        codeql_status=CodeQLStatus.ACTIVE if codeql_status == "active" else (
            CodeQLStatus.FAILURE if codeql_status == "failure" else CodeQLStatus.NONE
        ),
        last_commit_at=last_commit_at,
        commit_count=commit_count,
        readme_badges=badges
    )

    return Repository(
        name=name,
        full_name=repo_dict["full_name"],
        html_url=repo_dict["html_url"],
        description=repo_dict.get("description"),
        metrics=metrics
    )

async def _fetch_repos_from_cache_or_api(username: Optional[str]) -> List[Repository]:
    """Fetches repositories from cache or API."""
    cache_key = f"repos_{username or 'authed'}"
    cached = ttl_cache.get(cache_key)

    if cached:
        return list(cached)

    repos_data = await _fetch_user_repos_data(username)
    repositories = await asyncio.gather(*[fetch_repo_metrics(r) for r in repos_data])
    ttl_cache.set(cache_key, repositories)
    return list(repositories)

async def _fetch_user_repos_data(username: Optional[str]) -> List[Dict[str, Any]]:
    """Fetches repository data from GitHub API and filters by user."""
    repos_data = await github_client.get_user_repos(username)

    if username:
        target_login = username
    else:
        user_info = await github_client.get_authenticated_user()
        target_login = user_info.get("login", "")

    return [
        r for r in repos_data
        if r["owner"]["login"].lower() == target_login.lower()
    ]

def _apply_filters(
    repositories: List[Repository],
    filter_test: Optional[FilterValue],
    filter_quality: Optional[FilterValue],
    filter_codeql: Optional[FilterValue]
) -> List[Repository]:
    """Applies filters to the repository list."""
    if filter_test:
        repositories = [r for r in repositories if r.metrics and (
            (filter_test == FilterValue.PASS and r.metrics.build_status == BuildStatus.SUCCESS) or
            (filter_test == FilterValue.FAIL and r.metrics.build_status == BuildStatus.FAILURE)
        )]

    if filter_codeql:
        repositories = [r for r in repositories if r.metrics and (
            (filter_codeql == FilterValue.PASS and r.metrics.codeql_status == CodeQLStatus.ACTIVE) or
            (filter_codeql == FilterValue.FAIL and r.metrics.codeql_status == CodeQLStatus.FAILURE) or
            (filter_codeql == FilterValue.NONE and r.metrics.codeql_status == CodeQLStatus.NONE)
        )]

    if filter_quality:
        repositories = [r for r in repositories if r.metrics and (
            (filter_quality == FilterValue.PASS and len(r.metrics.quality_tools) > 0) or
            (filter_quality == FilterValue.FAIL and len(r.metrics.quality_tools) == 0)
        )]

    return repositories

def _apply_sorting(
    repositories: List[Repository],
    sort_by: Optional[str]
) -> List[Repository]:
    """Sorts the repository list."""
    if sort_by == "coverage":
        repositories.sort(
            key=lambda r: (r.metrics.coverage_percentage if r.metrics else 0) or 0,
            reverse=True
        )
    elif sort_by == "status":
        status_order = {
            BuildStatus.SUCCESS: 0,
            BuildStatus.IN_PROGRESS: 1,
            BuildStatus.UNKNOWN: 2,
            BuildStatus.FAILURE: 3
        }
        repositories.sort(
            key=lambda r: status_order.get(r.metrics.build_status if r.metrics else BuildStatus.UNKNOWN, 4)
        )
    elif sort_by == "last_commit":
        repositories.sort(
            key=lambda r: (r.metrics.last_commit_at if r.metrics else "") or "",
            reverse=True
        )
    return repositories

@router.get("/repos", response_model=List[Repository])
async def list_repos(query: RepoListQuery = Depends()):
    """Lists all repositories with metrics."""
    repositories = await _fetch_repos_from_cache_or_api(query.username)
    repositories = _apply_filters(
        repositories, query.filter_test, query.filter_quality, query.filter_codeql
    )
    repositories = _apply_sorting(repositories, query.sort_by)
    return repositories
