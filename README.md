# GitHub Repo Observatory

[![version](https://img.shields.io/badge/version-0.1.1-blue)](https://github.com/dgaida/github-repo-observatory)
[![codecov](https://codecov.io/gh/dgaida/github-repo-observatory/branch/main/graph/badge.svg)](https://codecov.io/gh/dgaida/github-repo-observatory)
[![tests](https://github.com/dgaida/github-repo-observatory/actions/workflows/ci.yml/badge.svg)](https://github.com/dgaida/github-repo-observatory/actions/workflows/ci.yml)
[![codeql](https://github.com/dgaida/github-repo-observatory/actions/workflows/codeql.yml/badge.svg)](https://github.com/dgaida/github-repo-observatory/actions/workflows/codeql.yml)
[![code quality](https://img.shields.io/badge/code%20quality-A-brightgreen)](https://github.com/dgaida/github-repo-observatory)
[![python](https://img.shields.io/badge/python-3.10%2B-blue)](https://github.com/dgaida/github-repo-observatory)
[![license](https://img.shields.io/badge/license-MIT-blue)](https://github.com/dgaida/github-repo-observatory/blob/main/LICENSE)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**One-line description**: Monitor CI health, test coverage, and code quality across all your GitHub repos in a single dashboard.

---

## 🚀 Quick Start

### For Users (Hosted Version)
1. Visit [observatory.example.com](https://observatory.example.com) (Placeholder)
2. Enter your GitHub username
3. View your repository health dashboard

### For Developers (Local Setup)
```bash
# Clone & install
git clone https://github.com/dgaida/github-repo-observatory.git
cd github-repo-observatory
pip install -r requirements.txt

# Configure
export GITHUB_TOKEN=ghp_your_token_here

# Run
uvicorn app.main:app --reload
```

## 📋 Prerequisites
- Python 3.10+
- GitHub Personal Access Token (read-only, public repos)

## ⚙️ Configuration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes | - | GitHub PAT with `repo` scope |
| `APP_PORT` | No | 10000 | Server port |
| `CACHE_TTL` | No | 3600 | Cache duration in seconds |
| `LOG_LEVEL` | No | INFO | Logging level |

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

## 🚀 Deployment

### Automatic Deployment to Render
The repository includes a GitHub Action to automatically deploy to [Render.com](https://render.com) on every push to the `main` branch.

**Setup:**
1. In your Render Dashboard, go to your service's **Settings** tab.
2. Scroll down to the **Deploy Hook** section and copy the URL.
   - It will look like `https://api.render.com/deploy/srv-<SERVICE_ID>?key=<TOKEN>`.
   - Yes, the service ID part starts with `srv-`.
3. In your GitHub repository, go to **Settings > Secrets and variables > Actions**.
4. Click **New repository secret** and add:
   - **Name**: `RENDER_DEPLOY_HOOK_URL`
   - **Value**: (The URL you copied from Render)

---

## 🧪 Running Tests
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest
```

---

## 🏗️ Project Structure

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
│   │   ├── metrics.py
│   │   └── enums.py            # Status and filter enums
│   │
│   ├── parsers/                # README, badge, and log parsing
│   │   ├── readme_parser.py
│   │   ├── shield_parser.py
│   │   └── action_logs.py
│   │
│   ├── cache/                  # Caching and rate-limit protection
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

## 🐛 Troubleshooting
**"GitHub API rate limit exceeded"**
- Ensure your `GITHUB_TOKEN` is set correctly
- Authenticated requests have 5000/hour limit vs 60/hour

---

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) (Placeholder) for guidelines.

---

## 📝 License
MIT License - see [LICENSE](LICENSE)
