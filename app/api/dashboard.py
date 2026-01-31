from fastapi import APIRouter, Request, Query, Depends
from fastapi.templating import Jinja2Templates
from typing import Optional
from .repos import list_repos
from ..models.requests import RepoListQuery
import os

router = APIRouter()

# Setup templates
templates_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/")
async def dashboard(
    request: Request,
    query: RepoListQuery = Depends()
):
    repos = await list_repos(query=query)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "repos": repos,
            "username": query.username,
            "sort_by": query.sort_by,
            "filter_test": query.filter_test,
            "filter_quality": query.filter_quality,
            "filter_codeql": query.filter_codeql
        }
    )
