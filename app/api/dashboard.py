from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from typing import Optional
from .repos import list_repos
import os

router = APIRouter()

# Setup templates
templates_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/")
async def dashboard(
    request: Request,
    username: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    filter_test: Optional[str] = Query(None),
    filter_quality: Optional[str] = Query(None),
    filter_codeql: Optional[str] = Query(None)
):
    repos = await list_repos(
        username=username,
        sort_by=sort_by,
        filter_test=filter_test,
        filter_quality=filter_quality,
        filter_codeql=filter_codeql
    )
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "repos": repos,
            "username": username,
            "sort_by": sort_by,
            "filter_test": filter_test,
            "filter_quality": filter_quality,
            "filter_codeql": filter_codeql
        }
    )
