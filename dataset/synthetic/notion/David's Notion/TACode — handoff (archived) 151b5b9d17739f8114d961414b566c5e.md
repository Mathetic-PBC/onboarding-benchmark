# TACode — handoff (archived)

Created: January 30, 2026 3:40 PM
Tags: archived, PRIME Lab
Status: Archived

Moved here from the handoff email thread in November 2025 so it lives somewhere searchable. I'm no longer on TACode; Rezky owns the backend and Yue owns the frontend as of 2025-11-14.

## Repos

| Repo | What | Owner now | State at handoff |
| --- | --- | --- | --- |
| `tacode` | React frontend: TA queue view, student code viewer, suggested-feedback panel | Yue | builds, 3 open PRs |
| `tacode_backend` | FastAPI + Postgres; queue, sessions, LLM feedback drafts | Rezky | deployed on the lab VM, nightly backup cron |

## How to run it locally

1. `docker compose up db` (Postgres 15)
2. `cd tacode_backend && uv sync && uv run alembic upgrade head && uv run uvicorn app.main:app --reload`
3. `cd tacode && pnpm i && pnpm dev` (expects the API on :8000)
4. Keys: the LLM key and the Canvas token are in the lab password vault under "TACode", **not** in `.env.example`.

## Known issues (as of handoff)

- Feedback drafts sometimes quote the wrong file when a student has two files with the same name in different folders (keyed by basename, should be full path).
- Queue position jumps when a TA reassigns a ticket; the websocket sends the old index. Repro in issue #41.
- Canvas roster sync fails silently if a section has zero students; add a log line.
- Alembic migration 0012 is not reversible. Don't downgrade past it.

## Decisions we made and why

- TAs approve every LLM draft before a student sees it. Non-negotiable after the pilot where one draft gave away the solution.
- No student code leaves the lab VM except the snippet sent to the model; we strip names and emails first.

## Open questions I left for Rezky and Yue

- Whether to keep the "suggested next hint" button or drop it (TAs said it was noisy).
- Whether to migrate off the lab VM before spring.

---

Archived 2026-01-30. Not touching this again unless someone asks.
