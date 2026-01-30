# GitHub Repo Observatory

**GitHub Repo Observatory** is a web-based dashboard that automatically analyzes all GitHub repositories of a user and aggregates CI health, test results, coverage, and code quality metrics into a single, continuously updated overview.

The service is fully hosted (no local startup required) and is intended for maintainers, educators, and teams who want a clear, high-level view of the technical health of their repositories.

---

## Features

- 📦 Automatic discovery of all GitHub repositories for a user or organization
- 🧪 CI status and failing test detection via GitHub Actions
- 📊 Test coverage extraction from README badges (e.g. Shields.io)
- 🛡 CodeQL workflow detection and status
- 🧹 Code quality badge detection (Code Climate, Sonar, etc.)
- ⚡ API rate-limit–aware caching
- 🌐 Browser-based dashboard (no authentication required)

---

## Architecture

The project follows a layered architecture with clear separation of concerns:

- **API Layer:** FastAPI endpoints (HTML dashboard + JSON API)
- **Service Layer:** GitHub integration, metrics aggregation, and parsing logic
- **Parsing Layer:** README badge parsing, Shields.io decoding, and workflow log analysis
- **Frontend:** Server-rendered dashboard (Jinja2 + minimal JS)

This structure is designed to scale as new metrics and data sources are added.

---

## Metrics Collected

For each repository, the dashboard collects:

- Repository name and link
- Build / workflow status
- Number of failing tests (when detectable)
- Test coverage (parsed from coverage badges)
- Presence and status of CodeQL analysis
- Presence of code quality tools (e.g. SonarCloud, Code Climate)

> The tool assumes that repositories use GitHub Actions and expose relevant badges in their `README.md`.

---

## Deployment (Render)

The application is designed to run on **Render** as a managed web service.

### Requirements

- Python 3.10+
- A GitHub Personal Access Token (read-only)

### Environment Variables

Set the following environment variable in Render:

```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

The token requires **read-only access** to public repositories.

### Start Command

```
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Build Command

```
pip install -r requirements.txt
```

---

## Local Development (Optional)

Although the project is intended to run hosted, it can also be started locally:

```
export GITHUB_TOKEN=ghp_xxx
uvicorn app.main:app --reload
```

Then open:

```
http://localhost:8000
```

---

## Project Structure

```
github-repo-observatory/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── config.py               # Configuration and environment handling
│   │
│   ├── api/                    # HTTP endpoints (HTML + JSON)
│   │   ├── dashboard.py
│   │   ├── repos.py
│   │   └── health.py
│   │
│   ├── services/               # Business logic and GitHub integration
│   │   ├── github_client.py
│   │   ├── actions_service.py
│   │   ├── coverage_service.py
│   │   ├── badge_service.py
│   │   └── quality_service.py
│   │
│   ├── models/                 # Domain and metric models
│   │   ├── repo.py
│   │   └── metrics.py
│   │
│   ├── parsers/                # README, badge, and log parsing
│   │   ├── readme_parser.py
│   │   ├── shield_parser.py
│   │   └── action_logs.py
│   │
│   ├── cache/                  # Caching and rate-limit protection
│   │   ├── memory_cache.py
│   │   └── ttl_cache.py
│   │
│   ├── frontend/               # Dashboard UI
│   │   ├── templates/
│   │   └── static/
│   │
│   └── utils/                  # Shared utilities
│       ├── rate_limit.py
│       └── logging.py
│
├── tests/                      # Automated tests
├── scripts/                    # Helper scripts (exports, local dev)
├── docs/                       # Architecture and metric documentation
├── .github/workflows/          # CI, CodeQL, deployment
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Roadmap

- Numeric coverage extraction from Shields.io badges
- Accurate failing test counts via workflow log analysis
- Sorting and filtering in the dashboard
- CSV / JSON export of metrics
- Organization-wide and multi-user support

---

## Use Cases

- Continuous quality monitoring of personal or organizational repositories
- CI health overview for teaching and academic projects
- Early detection of broken pipelines and missing quality checks

---

## License

MIT License

