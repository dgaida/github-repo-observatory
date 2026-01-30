from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import dashboard, repos, health
from .utils.logging import setup_logging
import os

# Initialize logging
setup_logging()

app = FastAPI(title="GitHub Repo Observatory")

@app.on_event("shutdown")
async def shutdown_event():
    from .services.github_client import github_client
    await github_client.close()

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "frontend", "static")
if not os.path.exists(static_path):
    os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(repos.router, prefix="/api", tags=["API"])
app.include_router(dashboard.router, tags=["Dashboard"])

if __name__ == "__main__":
    import uvicorn
    from .config import config
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)
