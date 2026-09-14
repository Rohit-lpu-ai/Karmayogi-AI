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
│   └── seed/              canonical dataset import (python -m app.seed)
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

The demo users are synthetic (`*@example.invalid`) and get the password `DEMO_USER_PASSWORD` from `.env`. `--demo-content` creates the labelled DEMO framework, job role, assessment and courses (local/ci only, DEC-045). The frontend is in `../frontend` (see its README).

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
