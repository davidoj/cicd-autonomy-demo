# cicd-autonomy-demo

A minimal FastAPI web service with a complete CI/CD pipeline, stood up end-to-end by an AI agent
(Claude Code) from a natural-language brief on 2026-07-04, as an empirical probe of autonomous
DevOps capability. No human edited code, config, or infrastructure; any human interventions are
documented in the section below.

## Architecture

- **Service**: FastAPI app (`app/main.py`) exposing `/` (service metadata: name, version,
  environment) and `/health`.
- **CI** (GitHub Actions): ruff lint + pytest on every push and pull request to `development`
  and `main`.
- **CD** (Render): `cicd-demo-staging` auto-deploys from `development`; `cicd-demo-prod`
  auto-deploys from `main`. `main` is a protected branch — changes land only via pull request
  with the CI check green, so production deploys are gated on tests.
- **Rollback**: demonstrated by shipping v2 to production through the pipeline, then reverting
  it through the same pipeline (see git history).

## Local development

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/pytest
.venv/bin/uvicorn app.main:app --reload
```

## Human interventions

(None yet — this section is updated honestly if the agent hits an authorization wall.)
