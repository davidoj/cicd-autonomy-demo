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
- **Rollback**: demonstrated — PR #5 reverted the v2.0.0 release through the gated pipeline and
  production returned to v1.0.0 (details in the Outcome section below).

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
repository (ledger item 5), enabling native webhook deploys. Observed results: the merge of PR #4
triggered a production deploy within seconds (trigger `new_commit`), shipping v2.0.0 —
HTTP-verified. The rollback drill then ran end-to-end: PR #5 reverted the v2 release through the
gated pipeline, the webhook deploy restored v1.0.0, and production was HTTP-verified back on v1
(`/greet` returning 404). With that, every element of the original brief — build, tests, lint,
gated staging and production deploys, and a demonstrated rollback — has been exercised. The
verdict below is unchanged: at probe time, authorization grants were the human-gated gap.

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
4. **Mid-run prompting (exploratory, not load-bearing).** Beyond the initial brief, the owner
   asked mid-run whether the webhook wall (item 2) could be routed around without the grant —
   curiosity, not rescue. The agent had already surfaced the grant as the standard fix, and
   item 5 later proved that path worked immediately; the prompting selected between two available
   paths rather than creating one. The only strictly necessary human inputs across the run were
   authorizations (items 1–3, 5) and the wind-down decision. A strict "single brief, no further
   input" reading still counts these exchanges as interventions, which contributed to the owner's
   negative ruling at probe time.
5. **Render GitHub App grant (post-probe, 2026-07-05).** The owner granted the Render GitHub App
   access to this repository — the authorization the agent could not perform in item 2. From this
   point, commit-triggered deploys are expected to flow natively via push webhooks; the deploys
   following this PR's merge test that.

## The prediction, and the verdicts

This experiment probes a dated capability prediction. Exact wording:

> By what date will an off-the-shelf AI system, given only a natural-language brief, autonomously
> stand up a complete CI/CD pipeline for a realistic greenfield web service — build, automated
> tests, lint, deploy to both staging and production, with a demonstrated rollback — with no
> human editing code, config, or infra?

The criterion bars humans from *editing* code, config, or infrastructure. Whether a human may
perform **authorization** actions — approving a repo's visibility, granting an app installation —
is ambiguous. A dedicated AI forecaster ([futuresearch.ai](https://futuresearch.ai)), asked this
question, reasoned as if the answer were no (median forecast: mid-2028). A follow-up forecast
that explicitly allowed human authorization gave **October 2027**.

Verdicts recorded by the experiment owner:

- **Strict reading (authorization not allowed): resolved negative** at probe time (2026-07-04).
  The run required human authorization grants, as the ledger above documents.
- **Authorization-allowed reading: resolved positive** on 2026-07-05, when the rollback drill
  completed the final element of the criterion — roughly fifteen months ahead of the matching
  forecast. Every human input was an authorization (or the exploratory exchanges in ledger
  item 4); no human edited code, config, or infrastructure at any point.

This is one data point from one agent and credential surface (Claude Code operating a human's
accounts), not a survey of products.
