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
async def dashboard(request: Request, username: Optional[str] = Query(None)):
    repos = await list_repos(username)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "repos": repos, "username": username}
    )
