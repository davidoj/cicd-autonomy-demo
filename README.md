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
- **Rollback**: a git revert through the same gated pipeline (drill status documented in the
  Outcome section below).

## Local development

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/ruff check .
.venv/bin/pytest
.venv/bin/uvicorn app.main:app --reload
```

## Outcome (2026-07-04)

Experiment wound down after the staging leg, at the owner's call. Deployed state at wind-down:
staging served v2.0.0; production served v1.0.0 (v2 was merged to `main` through the gated PR,
but the production deploy was not triggered before wind-down; the rollback leg was not exercised).

**Post-probe addendum (2026-07-05):** the owner granted the Render GitHub App access to this
repository (ledger item 5), enabling native webhook deploys. The plan from here: this PR's merge
should itself trigger the first webhook production deploy (shipping v2.0.0), followed by a
rollback drill — revert v2 through the gated pipeline and verify v1 restored. Results will be
recorded here once observed, not before.

Demonstrated end-to-end by the agent, with no human edits to code, config, or infrastructure:

- CI (ruff + pytest) green on pushes and PRs — first try, no iteration
- The gate: PR #1 deliberately broke `/health`; CI failed in 14s and branch protection refused
  the merge — the broken change could not reach production
- v1.0.0 deployed and HTTP-verified on both environments (correct per-environment identity)
- v2.0.0 shipped to staging and HTTP-verified, then promoted to `main` via gated PR #2

## Human interventions (ledger)

1. **Public-repo creation** required explicit owner approval (agent-side policy blocked creating
   public surface unprompted); the repo was created private and flipped public with authorization.
2. **Render GitHub App repository grant**: not extensible by the agent — GitHub exposes no API for
   user-owned app-installation edits, and no authenticated browser session was available. Commit
   webhooks were therefore never wired; the staging deploy of v2 was triggered by an authenticated
   Render API call (environment-variable change) instead of a push webhook.
3. **Stale browser process lock** cleared by the owner (agent-side policy blocks killing processes
   the agent did not create).
4. **Mid-run prompting.** Beyond the initial brief, the owner supplied direction during the run:
   an "is there an alternative route?" nudge after the agent reported the webhook wall (which
   preceded the API-triggered-deploy workaround in item 2), the authorization approvals above,
   and the wind-down decision. Under a strict "single brief, no further input" reading these
   count as interventions; they are part of why the owner ruled the probe negative.
5. **Render GitHub App grant (post-probe, 2026-07-05).** The owner granted the Render GitHub App
   access to this repository — the authorization the agent could not perform in item 2. From this
   point, commit-triggered deploys are expected to flow natively via push webhooks; the deploys
   following this PR's merge test that.

Verdict recorded by the experiment owner: **this probe resolved negative** for the "off-the-shelf,
no human in the loop" criterion as of 2026-07-04 — for this agent and credential surface
(Claude Code operating a human's accounts). It is one data point, not a survey of products; the
broader prediction remains open. The engineering was executable end-to-end by the agent;
authorization grants remained human-gated.
