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

from ..services.badge_service import BadgeService

async def fetch_repo_metrics(repo_dict):
    owner = repo_dict["owner"]["login"]
    name = repo_dict["name"]

    # Fetch metrics in parallel for each repo
    build_status_task = ActionsService.get_build_status(owner, name)
    coverage_task = CoverageService.get_coverage(owner, name)
    quality_tools_task = QualityService.get_quality_tools(owner, name)
    codeql_status_task = QualityService.get_codeql_status(owner, name)
    badges_task = BadgeService.get_all_badges(owner, name)
    last_commit_task = github_client.get_last_commit(owner, name)
    commit_count_task = github_client.get_commit_count(owner, name)

    (build_status, coverage, quality_tools, codeql_status,
     badges, last_commit, commit_count) = await asyncio.gather(
        build_status_task, coverage_task, quality_tools_task, codeql_status_task,
        badges_task, last_commit_task, commit_count_task
    )

    last_commit_at = None
    if last_commit and "commit" in last_commit:
        last_commit_at = last_commit["commit"]["committer"]["date"]

    metrics = RepoMetrics(
        build_status=build_status,
        coverage_percentage=coverage,
        quality_tools=quality_tools,
        codeql_status=codeql_status,
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

@router.get("/repos", response_model=List[Repository])
async def list_repos(
    username: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None), # coverage, status, last_commit
    filter_test: Optional[str] = Query(None), # pass, fail
    filter_quality: Optional[str] = Query(None), # pass, fail (simplified)
    filter_codeql: Optional[str] = Query(None) # pass, fail, none
):
    cache_key = f"repos_{username or 'authed'}"
    cached_repositories = ttl_cache.get(cache_key)

    if not cached_repositories:
        try:
            repos_data = await github_client.get_user_repos(username)

            # Determine target user login for filtering
            if username:
                target_login = username
            else:
                user_info = await github_client.get_authenticated_user()
                target_login = user_info["login"]

            # Filter repos that belong to the user
            repos_data = [r for r in repos_data if r["owner"]["login"].lower() == target_login.lower()]

            # Process all repositories in parallel
            cached_repositories = await asyncio.gather(*[fetch_repo_metrics(r) for r in repos_data])
            ttl_cache.set(cache_key, cached_repositories)
        except Exception:
            cached_repositories = []

    repositories = list(cached_repositories)

    # Apply Filtering
    if filter_test:
        repositories = [r for r in repositories if r.metrics and (
            (filter_test == "pass" and r.metrics.build_status == "success") or
            (filter_test == "fail" and r.metrics.build_status == "failure")
        )]

    if filter_codeql:
        repositories = [r for r in repositories if r.metrics and (
            (filter_codeql == "pass" and r.metrics.codeql_status == "active") or
            (filter_codeql == "fail" and r.metrics.codeql_status == "failure") or
            (filter_codeql == "none" and r.metrics.codeql_status == "none")
        )]

    if filter_quality:
        repositories = [r for r in repositories if r.metrics and (
            (filter_quality == "pass" and len(r.metrics.quality_tools) > 0) or
            (filter_quality == "fail" and len(r.metrics.quality_tools) == 0)
        )]

    # Apply Sorting
    if sort_by == "coverage":
        repositories.sort(key=lambda r: r.metrics.coverage_percentage or 0, reverse=True)
    elif sort_by == "status":
        status_order = {"success": 0, "in_progress": 1, "unknown": 2, "failure": 3}
        repositories.sort(key=lambda r: status_order.get(r.metrics.build_status, 4))
    elif sort_by == "last_commit":
        repositories.sort(key=lambda r: r.metrics.last_commit_at or "", reverse=True)

    return repositories
