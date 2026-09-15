# Backend

FastAPI modular monolith for the competency intelligence and learning platform
([docs/SYSTEM_ARCHITECTURE.md](../docs/SYSTEM_ARCHITECTURE.md)). Status: roadmap Phase 2 complete;
vertical slice 1 (login → assessment → gaps → recommendations) implemented on DEMO content. See [docs/IMPLEMENTATION_STATUS.md](../docs/IMPLEMENTATION_STATUS.md).

## Layout

```
backend/
├── app/
│   ├── main.py            app factory (create_app) and uvicorn entry point (app_factory)
│   ├── models.py          registry importing every module's tables
│   ├── core/              config, logging (JSON, redaction, correlation IDs), errors (problem+json),
│   │                      middleware (correlation ID, security headers), db (engine, base, mixins), vocab
│   ├── modules/
│   │   ├── platform/      /healthz, /readyz; Topic
│   │   ├── organization/  Organization, Department, JobRole
│   │   ├── identity/      User, UserAccessRole
│   │   ├── competency/    CompetencyFramework, CompetencyCluster, Competency, CompetencyLevel, RoleCompetency
│   │   ├── content/       SourceRecord
│   │   ├── recommendation/ Course, CourseTopic, CourseCompetency
│   │   └── governance/    AuditLog, record_audit()
│   └── seed/              canonical dataset import (python -m app.seed), demo packs, demo reset
├── migrations/            Alembic (the only way to change the schema)
└── tests/                 unit/ (no database) and db/ (PostgreSQL)
```

## Setup (Windows, Git Bash; adapt paths for other shells)

From the repository root:

```bash
cp .env.example .env                 # then set POSTGRES_PASSWORD and matching DATABASE_URL / TEST_DATABASE_URL
docker compose --env-file .env -f deploy/docker-compose.yml up -d db   # pgvector/pgvector:pg17 on 127.0.0.1:5433

cd backend
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.lock
.venv/Scripts/alembic upgrade head
.venv/Scripts/python -m app.seed --org-code local-demo --org-name "Local development organisation" --demo-users --demo-content
.venv/Scripts/python -m uvicorn --factory app.main:app_factory --reload
.venv/Scripts/python scripts/smoke_vertical_slice.py   # optional live journey (uses training-manager01 by default)
```

The demo users are synthetic (`*@example.invalid`) and get the password `DEMO_USER_PASSWORD` from `.env`. `--demo-content` applies the versioned DEMO content packs (local/ci only, DEC-045, DEC-052). The frontend is in `../frontend` (see its README).

On Windows, `start-dev.bat` in the repository root does all of this (database, migrations, backend, frontend) and `stop-dev.bat` stops the servers. It checks ports 8000 and 5173 first: a working server of this project is reused, anything else holding the port (including a crashed `uvicorn --reload`) is named and you are asked before it is stopped. Use another backend port with `set BACKEND_PORT=8010` before running it; the Vite proxy follows through `API_PROXY_TARGET`.

## Demo packs and reset (local/ci only)

| Task | Command (from `backend/`) |
|---|---|
| Apply missing or newer DEMO packs | `.venv/Scripts/python -m app.seed --org-code local-demo --org-name "Local development organisation" --demo-users --demo-content` |
| Reset one synthetic account so it can take the baseline again | `.venv/Scripts/python -m app.seed.demo_reset --org-code local-demo --email learner01@example.invalid` |
| Reset every synthetic account (and replay onboarding) | `.venv/Scripts/python -m app.seed.demo_reset --org-code local-demo --all-synthetic --clear-job-role` (or `reset-demo.bat`) |

Packs are listed in `app/seed/demo_packs.py`; `seed_pack_applications` records the version applied per organisation. A pack's `apply` must be additive, and raising its `version` makes the next seed run apply it again. The reset never deletes history: attempts become `voided`, their evidence rows are voided, current estimates are removed and the action is audited. It refuses non-synthetic accounts and any environment other than `local`/`ci` (DEC-052).

## Tests

```bash
cd backend
.venv/Scripts/python -m pytest            # all tests; db tests use TEST_DATABASE_URL
.venv/Scripts/python -m pytest -m "not db"  # without a database
```

Database tests reset the `public` schema of the test database and refuse to run unless its name ends in `_test`.
The Phase 1 tests still run from the repository root with `python -m unittest discover -s tests -t .`.

## Configuration

| Variable | Purpose |
|---|---|
| `APP_ENV` | `local`, `ci`, `staging`, `pilot`, `production`; OpenAPI is served only in `local`/`ci` (DEC-030) |
| `LOG_LEVEL` | `DEBUG` … `CRITICAL` |
| `DATABASE_URL` | `postgresql+psycopg://…`; held as a secret, never logged |
| `TEST_DATABASE_URL` | test database (name must end in `_test`) |
| `IGOT_CLIENT_MODE` | `mock` (default) or `live` (refused) |
