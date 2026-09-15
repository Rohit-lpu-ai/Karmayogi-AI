# Implementation Status

| Field | Value |
|---|---|
| **Version** | 1.5.0 (after product upgrade phase C: login, dashboard, competencies, gaps, catalogue, course detail, demo-2) |
| **Last verified** | 2026-09-15 |
| **Verified on** | Branch `Diw`, HEAD `0b2f86d` (vertical slice 1 committed). Product upgrade phases A, B and C are **uncommitted** in the working tree |
| **Related** | [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [AGENT_CONTEXT.md](AGENT_CONTEXT.md) · [FEATURE_CATALOG.md](FEATURE_CATALOG.md) · [DECISIONS.md](DECISIONS.md) |

## Status vocabulary

| Status | Meaning |
|---|---|
| **Implemented** | Code exists in the repository **and** a passing automated test exercises it |
| **Partially implemented** | Some required behaviour exists with evidence; named parts are missing |
| **Mocked** | Behaviour is provided by synthetic, labelled MOCK data only |
| **Missing** | No code exists |
| **Unknown** | Could not be determined from the repository or environment |
| **Blocked** | Cannot proceed without an external action, access or decision (named) |

This vocabulary describes **implementation**. Data provenance uses [../STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md) (DEC-017). The two are never mixed.

---

## 1. Verification performed

| Check | Command or method | Result |
|---|---|---|
| Repository inventory | `git ls-files`, `git status` | 117 committed files; 18 staged documentation files; no `backend/`, `frontend/` or `deploy/` directory |
| Existing tests | `python -m unittest discover -s tests -t .` | **35 tests, all pass** (7.3 s) |
| Canonical dataset validator | `python scripts/validators/validate_canonical_datasets.py` | Verdict `VALID_FOR_DEVELOPMENT_NOT_RELEASABLE`; 0 errors; release blockers LP-19 (696), LP-20 (7), LP-21 (21) |
| Raw documents | `find data/raw -name "*.pdf"` | 19 PDFs present locally (git-ignored) |
| Python | `python --version` | 3.11.9 |
| Python packages (global, no manifest) | `pip list` | fastapi 0.136.3, SQLAlchemy 2.0.51, alembic 1.17.1, pydantic 2.13.4, pydantic-settings 2.1.0, psycopg2-binary 2.9.9, uvicorn 0.46.0, httpx 0.28.1, pypdf 6.18.1, jsonschema 4.26.0. **Not installed:** pytest, argon2-cffi, pgvector, python-docx |
| Node | `node --version`, `npm --version` | Node 24.15.0, npm 11.12.1; pnpm not installed |
| PostgreSQL (host) | `pg_isready`, extension directory | PostgreSQL 18 service running on `localhost:5432`; `pgcrypto` and `citext` available; **`vector` (pgvector) not installed**; credentials not available to the agent |
| Docker | `docker info` | Docker Desktop 29.5.3; daemon was stopped and was started during verification |
| Redis | `command -v redis-server` | Not installed |
| Referenced documents | `ls docs/*.md` | 9 referenced documents missing (§4) |

## 1a. Verification after Phase 2

| Check | Command | Result |
|---|---|---|
| Backend tests | `cd backend && .venv/Scripts/python -m pytest` | **73 passed**, 0 skipped (unit tests + tests against PostgreSQL 17.11) |
| Phase 1 tests | `python -m unittest discover -s tests -t .` | **35 passed** (unchanged) |
| Migrations on dev database | `alembic upgrade head` | `0001`, `0002` applied |
| Seed run 1 | `python -m app.seed --org-code local-demo ... --demo-users` | 23 topics, 1 framework, 4 clusters, 25 competencies, 5 levels, 100 source records, 99 courses, 111 course-topic suggestions, 1 department, 8 synthetic users; warning for CSCD-2014-4.8 |
| Seed run 2 | same command | 0 created |
| API smoke | `uvicorn --factory app.main:app_factory`; requests to `/readyz` and an unknown route | 200 with correlation ID and security headers; 404 `application/problem+json` |
| Local database | `docker compose --env-file .env -f deploy/docker-compose.yml up -d db` | `pgvector/pgvector:pg17` healthy on `127.0.0.1:5433`; `vector` 0.8.6 available, not enabled |

Section 2 below reflects the state after Phase 2.

## 1b. Verification after vertical slice 1 (2026-09-15)

Full command output: [evidence/implementation/vertical-slice-1/](evidence/implementation/vertical-slice-1/). Plan and pre-implementation verification: [VERTICAL_SLICE_1_PLAN.md](VERTICAL_SLICE_1_PLAN.md).

| Check | Command | Result | Evidence |
|---|---|---|---|
| Re-verification of Phase 2 claims | git, alembic, psql, pytest | All functional claims held; 4 stale status statements corrected | `01`-`04` |
| Backend tests | `cd backend && .venv/Scripts/python -m pytest -v` | **167 passed**, 0 failed, 0 skipped | `07-backend-tests.txt` |
| Phase 1 tests | `python -m unittest discover -s tests -t .` | 35 passed | `03`, final run in report |
| Migration `0003` on dev database | `alembic upgrade head`; `alembic check` | Applied; no model drift | `08` |
| Demo seed | `python -m app.seed … --demo-users --demo-content` (twice) | Run 1: 8 passwords, 1 framework, 4 levels, 2 competencies, 1 job role, 2 mappings, 10 questions, 1 assessment, 3 courses, 4 course mappings. Run 2: nothing | `08` |
| Live API journey | `scripts/smoke_vertical_slice.py` against uvicorn | Login → notice → role → attempt → submit → result → gaps → recommendations → logout; CSRF-missing 403; double submit 409 | `09` |
| Frontend type-check, tests, build | `npm run typecheck`, `npm test`, `npm run build` | 0 type errors; **12 passed**; build 202.89 kB JS (65.56 kB gzip) | `11` |
| Journey through the Vite dev proxy | smoke script with `SMOKE_BASE_URL=http://localhost:5173` | Same journey passes through the proxy with cookies | `12` |
| Dependency audit | `npm audit` | 0 vulnerabilities (after replacing React Router 6 / Vitest 3, DEC-048) | `10` |
| Log hygiene | grep of the API log | 0 occurrences of the demo password, session cookie or email addresses | `13` |
| Browser walkthrough | — | **Not performed** (no browser automation available in this session) | — |

## 1c. Verification after product upgrade phase A (2026-09-15)

Baseline audit: [evidence/implementation/product-upgrade-baseline.md](evidence/implementation/product-upgrade-baseline.md). Phase A evidence and screenshots: [evidence/implementation/product-upgrade-phase-a/](evidence/implementation/product-upgrade-phase-a/).

| Check | Command | Result | Evidence |
|---|---|---|---|
| Backend tests | `cd backend && .venv/Scripts/python -m pytest -q` | **180 passed** (167 before + 13 for demo packs and reset), 0 failed | `03` |
| Migration `0004` | `alembic upgrade head`, `alembic check`, `alembic downgrade 0003`, `alembic upgrade head` | Applied, reversible, no drift. Note: the downgrade step, run on the dev database, turned one voided demo attempt into `expired` as designed | `04` |
| Phase 1 tests | `python -m unittest discover -s tests -t .` | 35 passed | `05` |
| Frontend | `npm run typecheck`, `npm test`, `npm run build`, `npm audit` | 0 type errors; **22 passed** (12 before + 10 shell/component tests); build JS 373 kB (119 kB gzip, was 203/66 kB: Radix, sonner, lucide), CSS 34 kB; 0 vulnerabilities | `06` |
| Launcher port detection | `deploy/local/dev-port.ps1` on this project's API, this project's Vite, the wrong kind, a stale `uvicorn --reload` in `Bound` state, and a free port | exit 10, 10, 20, 20, 0 as designed | `01` |
| Journey through the Vite proxy with `API_PROXY_TARGET` | `SMOKE_BASE_URL=http://localhost:5173 scripts/smoke_vertical_slice.py department-admin01@example.invalid` (backend on 8001) | Full journey passes; the account had been reset, so the reset allowing a new baseline is shown live | `02` |
| Proxy with backend down | `API_PROXY_TARGET=http://127.0.0.1:8999` + request to `/api/v1/auth/session` | 503 `application/problem+json`, code `BACKEND_UNAVAILABLE` | this table |
| Demo packs on the dev database | `python -m app.seed ... --demo-users --demo-content` | `demo-1` adopted, nothing re-created | this table |
| Screenshots | headless Microsoft Edge via DevTools protocol (the Claude-in-Chrome extension was not connected) | 9 screenshots: login desktop/360 px, dashboard desktop/360 px, demo notice, account menu, mobile menu, assessment, design system | `screenshots/` |
| Automated accessibility (axe), Playwright journeys, screen-reader test | - | **Not performed** (tooling not adopted yet) | - |

## 1d. Verification after product upgrade phase B (2026-09-15)

Evidence and 19 screenshots: [evidence/implementation/product-upgrade-phase-b/](evidence/implementation/product-upgrade-phase-b/). No backend contract changed.

| Check | Command | Result | Evidence |
|---|---|---|---|
| Browser journeys with axe | `cd frontend && CAPTURE_SCREENSHOTS=1 npx playwright test` (Edge, 1440 px and 360 px; stack: backend on 8001, Vite with `API_PROXY_TARGET`) | **6 passed**: onboarding with keyboard and focus checks; assessment with keyboard answers, reload resume, question grid, confirmation, submit; result with disclosures and next-step link. 0 serious/critical axe violations on 9 checked states; no horizontal page scroll | `01` |
| Frontend | `npm run typecheck`, `npx vitest run`, `npm run build`, `npm audit` | 0 type errors; **37 passed** (6 files); JS 438 kB (136 kB gzip); 0 vulnerabilities | `02` |
| Backend tests | `.venv/Scripts/python -m pytest -q` | **180 passed** (unchanged; no backend code change except the test helper script) | `03` |
| Live journey through the Vite proxy | `SMOKE_BASE_URL=http://localhost:5173 scripts/smoke_vertical_slice.py department-admin01@example.invalid` (account reset afterwards) | Passes | `04` |
| Manual screen-reader test (NVDA/JAWS) | - | **Not performed** | - |

Defects found and fixed during phase B: answering a question without `?q=` moved the learner to the next unanswered question (starting position now pinned in the URL); option letters followed original keys in shuffled order (now positional); `<dl>` markup failed axe `definition-list`/`dlitem` on the onboarding assessment step; avatar initials used punctuation.

## 1e. Verification after product upgrade phase C (2026-09-15)

Plan and decisions: [evidence/implementation/phase-c-plan.md](evidence/implementation/phase-c-plan.md). Lessons proposal (awaiting approval): [evidence/implementation/phase-c-learning-experience-proposal.md](evidence/implementation/phase-c-learning-experience-proposal.md). Evidence and screenshots: [evidence/implementation/product-upgrade-phase-c/](evidence/implementation/product-upgrade-phase-c/).

| Check | Command | Result | Evidence |
|---|---|---|---|
| Browser journeys with axe | `cd frontend && npx playwright test` (Edge; 1440 px and 360 px) | **10 passed**: login; learner loop (dashboard before and after baseline, competency profile, gap analysis with table view, catalogue with keyboard filter and search, course detail); onboarding; assessment; result. 0 serious/critical axe violations on every checked state; no horizontal page scroll | `01` |
| Frontend | `npm run typecheck`, `npx vitest run`, `npm run build`, `npm audit` | 0 type errors; **46 passed** (7 files); JS 501 kB (150 kB gzip, above Vite's 500 kB warning); 0 vulnerabilities | `02` |
| Backend tests | `.venv/Scripts/python -m pytest -q` | **196 passed** (16 new: demo-2 content and journey, difficulty never changes ranking, catalogue filters/visibility/authorisation, course detail, attempt history) | `03` |
| Migrations | `alembic current`, `alembic check`; `0005` upgrade/downgrade cycle run during development | `0005 (head)`, no drift | `04` |
| Live API journey through the Vite proxy | `smoke_vertical_slice.py department-admin01@example.invalid` (account reset afterwards) | Passes | `05` |
| Demo packs on the dev database | `python -m app.seed ... --demo-content` | `demo-2` applied: 1 framework, 4 levels, 8 competencies, 40 questions, 3 roles, 12 role mappings, 3 assessments, 12 courses, 23 course mappings | this table |
| Manual screen-reader review | - | **Not performed** (DEC-056 D-6) | - |

## 1f. Phase 4A - accounts and administration (2026-09-15)

Plan: [evidence/implementation/phase-4-plan.md](evidence/implementation/phase-4-plan.md). Screenshots: [evidence/implementation/phase-4a/screenshots/](evidence/implementation/phase-4a/screenshots/). Decisions DEC-057, DEC-058.

Built: learner / administration sign-in modes; learner registration (local/ci only); set-password via one-time link; profile with password change; administration area with its own navigation and route guard; admin overview, users (search, filters, add, manage status and roles, password links) and roles and permissions matrix; capability policy enforced on the server; migration 0006.

| Check | Result |
|---|---|
| Backend `pytest -q` | **234 passed** (38 new in `tests/db/test_accounts_admin_api.py`: registration on/off, duplicates, validation, no password in logs, password change and one-time tokens, admin authorisation matrix, department scoping, organisation isolation, audit of role changes) |
| Migrations | `0006 (head)`; upgrade/downgrade/upgrade cycle run; `alembic check` no drift |
| Frontend | typecheck clean; **62 passed** Vitest (15 new in `Phase4A.test.tsx`); build 557 kB JS (Vite size warning) |
| Browser journeys (Edge, 1440 px and 360 px, axe) | **16 passed**: 3 new Phase 4A journeys plus the 5 earlier journeys, 0 serious/critical axe violations, no horizontal scroll, no unexpected failed responses |
| Manual screen-reader review | Not performed (DEC-056 D-6) |

Known limitations: no email delivery (links are handed over manually); registration outside local/ci awaits D4-1; journeys leave `e2e-*@example.invalid` accounts in the local database (registered accounts are non-synthetic by design, so `demo_reset` does not remove them).

## 1g. Phase 4B - learning core (2026-09-15)

Decision DEC-059. Screenshots: [evidence/implementation/phase-4b/screenshots/](evidence/implementation/phase-4b/screenshots/).

Built: modules and lessons (synthetic pack `demo-3`: 12 courses, 24 modules, 48 lessons), course learning hub (`/courses/:id/learn`), lesson player (`/courses/:id/lessons/:lessonId`) with contents drawer on mobile, self-reported completion, resume, course completion, learning path (`/learning-path`, rule `path-v1`), assessment history (`/me/attempts`), progress on catalogue cards and filter, course detail structure and Start/Continue, dashboard Continue learning; demo reset clears learning progress; route-level code splitting.

| Check | Result |
|---|---|
| Backend `pytest -q` | **255 passed** (21 new: 8 `path-v1` unit tests, 13 learning API tests incl. isolation, no estimate change, append-only activity, concurrent open/complete) |
| Migrations | `0007 (head)`; upgrade/downgrade/upgrade cycle; `alembic check` no drift |
| Frontend | typecheck clean; **70 passed** Vitest (8 new); build: main JS 447 kB, admin and learning pages in separate chunks |
| Browser journeys (Edge, 1440 px and 360 px, axe) | **18 passed** including the new learning journey (baseline -> path -> course -> every lesson -> completion -> catalogue filter -> dashboard -> history) |
| Bug found and fixed | Opening and completing a lesson at the same moment raised a unique-constraint error (500); progress rows now use insert-if-absent with a row lock |

## 1h. Phase 4C - content and administration (2026-09-15)

Decision DEC-060. Screenshots: [evidence/implementation/phase-4c/screenshots/](evidence/implementation/phase-4c/screenshots/).

Built: question bank, authoring with versions and source metadata, review queue with the self-approval block, course administration (details, modules, lessons with Markdown preview, competency links, guard checklist, submit, publish, unpublish), competency structure view, assessment coverage and quality checks, audit trail with filters and paging; 22 source documents imported as reference-only source records; migration 0008.

| Check | Result |
|---|---|
| Backend `pytest -q` | **276 passed** (21 new: 20 content administration API tests - authorisation per capability, CSRF, question workflow incl. self-approval denial and audit, validation, retire guard, course guards and visibility, request-changes reason, views, audit paging - plus a model-registry regression test) |
| Migrations | `0008 (head)`; upgrade/downgrade/upgrade cycle; `alembic check` no drift |
| Frontend | typecheck clean; **75 passed** Vitest (5 new) |
| Browser journeys (Edge, 1440 px and 360 px, axe) | **24 passed**, including question authoring -> review by another person, course preparation -> review -> publish -> visible to a learner -> unpublished again, and governance screens |
| Bugs found and fixed | Missing model registry in the running app (500 on first question save); sign-out handing the next user the previous user's page; toasts covering form actions (moved to the top right) |

Known limitations: assessments cannot yet be assembled or versioned in the UI; review is single-reviewer (D4-5); journeys leave unpublished "Units and footnotes clinic ..." test courses and approved test questions in the local database.

## 1i. Phase 4D - insight, AI boundary and final verification (2026-09-15)

Decisions DEC-061, DEC-062. AI analysis: [evidence/implementation/phase-4-ai-boundary.md](evidence/implementation/phase-4-ai-boundary.md). Report: [evidence/implementation/phase-4-report.md](evidence/implementation/phase-4-report.md). Screenshots (final run of every journey): [evidence/implementation/phase-4d/screenshots/](evidence/implementation/phase-4d/screenshots/).

| Check | Result |
|---|---|
| Backend `pytest -q` | **289 passed** (13 new: 8 insight API incl. suppression, scoping, no personal data; 5 AI-boundary unit tests) |
| Migrations | `0008 (head)`, `alembic check` no drift (no 4D migration) |
| Frontend | typecheck clean; **77 passed** Vitest (11 files); build: main JS 453 kB (130 kB gzip), admin, learning and insight pages in separate chunks; `npm audit` 0 vulnerabilities |
| Browser journeys (Edge, 1440 px and 360 px, axe) | **26 passed** (13 journeys x 2 viewports), 0 serious/critical axe violations, no horizontal page scroll, no unexpected failed responses or console errors |
| Live API journey through the Vite proxy | `smoke_vertical_slice.py department-admin01@example.invalid` passes (account reset before and after) |
| Server log scan | 0 occurrences of the demo password, cookies, set-password tokens or password hashes in 3,442 log lines |
| Manual screen-reader review | **Not performed** (DEC-056 D-6) |

## 2. Component status

### 2.1 Platform foundation

| Component | Status | Evidence |
|---|---|---|
| Backend application (FastAPI) | Implemented (foundation) | `backend/app/main.py` app factory; `backend/tests/unit/test_http_foundation.py` |
| Configuration / settings module | Implemented | `backend/app/core/config.py` (typed, secrets as `SecretStr`, validated at startup); `tests/unit/test_config.py` |
| Structured logging with correlation IDs | Implemented | `backend/app/core/logging.py`, `middleware.py` (JSON; redacts secret keys, emails, phone numbers, 12-digit IDs, URL credentials); `tests/unit/test_logging.py` |
| Error handling (problem+json) | Implemented | `backend/app/core/errors.py`; unhandled errors hide details; `tests/unit/test_http_foundation.py` |
| Health and readiness endpoints | Implemented | `/healthz`, `/readyz` (database check) in `backend/app/modules/platform/api.py`; readiness tested with and without a database |
| PostgreSQL connection | Implemented | `backend/app/core/db.py` (psycopg 3, pooled, connect timeout); `tests/db/test_migrations.py::test_readyz_ok_with_database` |
| Alembic migrations | Implemented | `backend/migrations/versions/` `0001` (extensions), `0002` (reference schema and triggers); upgrade, downgrade to base and model sync tested |
| SQLAlchemy models | Partially implemented | Reference schema (16 tables) in `backend/app/modules/*/models.py`; assessment, content, AI and progress entities come in later phases |
| Dependency manifest | Partially implemented | `backend/pyproject.toml`, `backend/requirements.lock`; `scripts/` still has no manifest |
| Local database with pgvector | Implemented (local) | `deploy/docker-compose.yml` (`pgvector/pgvector:pg17`, port 5433, separate `platform_test` database); host PostgreSQL 18 untouched (DEC-037) |
| Background job infrastructure | Missing | No queue; estimates recomputed synchronously on submit (DEC-047) |
| Local launcher | Implemented (Windows, local) | `start-dev.bat`, `stop-dev.bat`, `reset-demo.bat`, `deploy/local/dev-port.ps1` (port ownership detection); verified manually (`evidence/implementation/product-upgrade-phase-a/01`) |
| Versioned DEMO packs and local demo reset | Implemented (local/ci only) | `backend/app/seed/demo_packs.py`, `demo_reset.py`, migration `0004`; `tests/db/test_demo_packs_and_reset.py` (DEC-052) |
| Object storage interface | Missing | — |
| CI pipeline | Missing | No `.github/workflows/` |

### 2.2 Domain modules

| Component | Status | Evidence |
|---|---|---|
| Organisations, departments | Partially implemented | Tables and seed; no administration API |
| Users, access roles | Partially implemented | `GET /me`, notice acknowledgement, job-role selection; synthetic users with passwords from `DEMO_USER_PASSWORD`. No user administration API |
| Authentication and sessions | Partially implemented | `identity/{security,service,dependencies,api}.py`: Argon2id, hashed server-side sessions, idle/absolute timeout, HMAC CSRF, lockout, logout. Missing: password change/reset, re-authentication, revoke-all, IP rate limiting |
| RBAC policy | Partially implemented | Default-deny session requirement on all slice routes; `require_any_role` (auditor/platform_admin excluded from learning); ownership checks (404 for other users' attempts); organisation scoping. Missing: full permission matrix, user/role administration APIs, authorisation test matrix for all endpoints |
| Audit logging | Partially implemented | Append-only table; events `auth.login.success`, `auth.login.failure`, `auth.lockout`, `auth.logout`, `user.job_role.change`, `attempt.submit`, `seed.import` (tested). No auditor API or UI |
| Job roles | Partially implemented | `GET /job-roles`, `PUT /me/job-role`; one DEMO job role (DEC-045). No official job roles; no admin CRUD |
| Competency frameworks | Partially implemented | Tables with restricted-definition, level-order and required-level triggers; CSCD structure imported as a `draft`, restricted framework (no definitions, provisional levels); no API (Phase 4) |
| Functional statistical competency framework | Blocked | No source exists (DEC-013); requires SME authoring |
| Role-to-competency requirements | Partially implemented (DEMO only) / Blocked for real data | `GET /job-roles/{id}/competencies` returns approved mappings; only DEMO mappings exist. Official mappings still blocked (ROLE-002, DEC-013) |
| Topic taxonomy | Partially implemented | 23 topics imported (`ASSUMED`, `unreviewed`); no API |
| Course catalogue | Partially implemented | 99 NSSTA listings imported with SourceRecord provenance (`unreviewed`, no dates, topic tags as suggestions); `course_competencies` empty (no approved mappings); no API (Phase 7) |
| Question bank, assessments, attempts, scoring | Partially implemented | `assessment/{models,service,api}.py`: approved-version delivery, seed-reproducible order, key-free responses, answer save, transactional submit, result feedback. Items are DEMO arithmetic only. Missing: authoring, blueprint editor, publishing API, review workflow, citations, rescoring |
| Competency estimation, gaps, evidence, explanations | Partially implemented | `competency/scoring.py` (pure `score-v1`, unit-tested), append-only evidence ledger, `user_competencies` with explanation blocks, `GET /me/competency-profile`, `GET /me/competency-gaps`. Missing: adjustments, correction requests, snapshots, staff views |
| Learning materials, upload, validation | Partially implemented | Offline collector with signature and size checks (`scripts/collectors/fetch_documents.py`). No upload API |
| Text extraction | Partially implemented | Offline pypdf metadata/text extraction (`scripts/utils/extract_pdf_metadata.py`). No application pipeline |
| Chunking, embeddings, pgvector storage | Missing | — |
| Semantic and keyword search | Missing | — |
| Grounded Q&A, citations | Missing | — |
| LLM and embedding provider interfaces | Missing | No AI code, no prompts |
| MCQ generation, validators, duplicate detection | Missing | — |
| Human review workflow | Missing | — |
| Recommendations, learning paths | Partially implemented / Missing | `recommendation/rules.py` (pure `rec-v1`), `GET /me/recommendations` computed on read from approved mappings (DEMO courses only). Missing: persistence, feedback, learning paths, catalogue review API |
| Progress tracking | Missing | — |
| Reports | Missing | — |

### 2.3 Integrations

| Component | Status | Evidence |
|---|---|---|
| `IGotClient` interface, records, errors, factory | Implemented | `clients/igot_client.py`; `tests/test_mock_igot_client.py` |
| Mock iGOT client | Mocked | `clients/mock_igot_client.py` over `data/samples/mock/MOCK_igot_fixtures.json`; refuses non-MOCK fixtures; 14 tests pass |
| `live` mode refusal | Implemented | `create_igot_client()` raises `AccessNotVerifiedError`; tested |
| Health / mode reporting on the interface | Missing | Planned for Phase 10 (DEC-021) |
| Integration health endpoint, IntegrationConnection | Missing | — |
| Real iGOT adapter, sync, deep links | Blocked | No documented API or authorised access ([../IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md)) |

### 2.4 Frontend

| Component | Status | Evidence |
|---|---|---|
| React application | Partially implemented | `frontend/` (React 18, TypeScript, Vite 8, React Router 7): login, get started (notice + job role), assessment, result, dashboard; Vitest tests in `src/pages/pages.test.tsx`, `src/api/client.test.ts`, `src/components/layout/AppShell.test.tsx`; production build; rendered in headless Edge (screenshots, phase A) |
| Login, dashboard, competency profile, gap analysis, course catalogue, course detail | Implemented (DEMO content) | `frontend/src/pages/LoginPage.tsx`, `DashboardPage.tsx`, `competencies/`, `courses/`; `GET /me/attempts`, `GET /courses`, `GET /courses/{id}` in `backend/app/modules/{assessment,recommendation}`; Vitest `PhaseC.test.tsx`; pytest `test_catalogue_api.py`, `test_demo_pack_2.py`; Playwright `e2e/learner-loop.spec.ts`. Lessons, learning path and progress: **not implemented** (awaiting DEC-056 D-3) |
| Learner onboarding, assessment and result screens | Implemented (frontend, DEMO content) | `src/pages/OnboardingPage.tsx`, `src/pages/assessment/`, `src/pages/results/`; Vitest `OnboardingPage.test.tsx`, `Assessment.test.tsx`, `Result.test.tsx`; Playwright `e2e/*.spec.ts`. Time per assessment is a rough guide derived from the question count (no duration field in the API) |
| Design system, screens | Partially implemented | Tailwind CSS 4 + shadcn/ui-style components on Radix (DEC-050): tokens with computed contrast ratios (`src/styles/globals.css`), base components (`src/components/ui/`), `AppShell` with sidebar, top bar, mobile drawer and account menu, `PageHeader`, `Breadcrumbs`, `StatCard`, `EvidenceBadge`, `DemoDataNotice`, `ConfirmationDialog`, toasts; dev-only gallery `/dev/design-system`. Learner screens still use scoped legacy styles inside the new shell. No i18n catalogue, no axe checks |

### 2.5 Data tooling (Phase 1)

| Component | Status | Evidence |
|---|---|---|
| Manifest-based document collector | Implemented | `scripts/collectors/fetch_documents.py`, manifests in `scripts/collectors/manifests/` |
| Canonical dataset build | Implemented | `scripts/processing/build_canonical_datasets.py` |
| Canonical dataset JSON Schema | Implemented | `schemas/canonical_datasets.schema.json` |
| Canonical dataset validator | Implemented | `scripts/validators/validate_canonical_datasets.py`; `tests/test_canonical_datasets.py` (21 tests) |
| Feature catalogue generator | Implemented (documentation tooling) | `scripts/docs/generate_feature_catalog.py`; no tests |
| Documentation consistency checker | Missing | `scripts/docs/check_docs_consistency.py` is cited by DEC-018 but absent |

## 3. Dataset schema versus DATA_MODEL.md

Required by the database rules before any model is built. All five datasets share the envelope `schema_version 0.2.0`, `dataset_id`, `generated_at_utc`, `inputs[{path, sha256}]`, `record_count`, `records`.

| Dataset field | DATA_MODEL target | Match | Resolution |
|---|---|---|---|
| Record `id` (string, e.g. `CSCD-2014-1.1`, `NSSTA-PRG-59f603f37c`) | `SourceRecord.canonical_record_id`; application PKs are UUIDs | Convention differs by design | Canonical IDs are kept as provenance keys, never used as primary keys (DEC-040) |
| `provenance.source_id` | `SourceRecord.registry_source_id` | Yes | Direct |
| `provenance.local_file_path` | `SourceRecord.raw_local_path` | Name differs | Mapped |
| `licence.usage_notes` | `SourceRecord.licence_notes` | Name differs | Mapped |
| `licence.permits_learner_display` (`null`) | `LearningMaterial.learner_display_permitted` (boolean, default false) | Type differs | `null` imports as `false` |
| `review.verified` | `SourceRecord.review_verified` | Yes | Direct |
| Competency `definition` (always `null`) | `Competency.description` (must be null when restricted) | Name differs | Mapped; the importer refuses non-null values for restricted frameworks |
| Competency `source_pages.definition` / `.detail` | `definition_source_page` / `detail_source_page` | Yes | Direct |
| Competency `proficiency_levels` (per record) | `CompetencyLevel` (per framework) | Granularity differs | Levels created once per framework from `framework.proficiency_scale`; the importer checks every record uses the same scale |
| Framework `id` `CSCD-2014` | `CompetencyFramework.code` | Yes | Direct |
| (none) | `CompetencyFramework.version_label` (required) | **Missing in dataset** | Use `2014` from the framework ID and record the derivation in the SourceRecord; not a guessed publication version (DEC-040) |
| Framework `publication_date` | (no column) | **Missing in model** | Not stored; available through the source document record. Flagged for DATA_MODEL review |
| (none) | `CompetencyLevel.min_score` | **Missing in dataset** | `null`, `threshold_status='provisional'` (DEC-020) |
| Topic `id` | `Topic.code` | Name differs | Mapped |
| Topics envelope `taxonomy_version` | `Topic.taxonomy_version` | Yes | Copied to each row |
| Topic `rule_count` | (no column) | Not needed | Dropped |
| Programme `provider` | `Course.provider_organisation` | Name differs | Mapped |
| Programme `delivery.duration_days_per_occurrence` | `Course.duration_days` | Name differs | Mapped |
| Programme `delivery.batch_size.min/max` | `batch_size_min/max` | Yes | Direct |
| Programme `delivery.venue_as_printed` | `Course.venue` | Name differs | Mapped |
| Programme `schedule.status_in_source` | `Course.schedule_status` | Name differs | Mapped |
| Programme `schedule.dates` (`null`) | (no column) | Consistent | Dates are never invented |
| Programme `programme_type_as_printed`, `topic_as_printed`, `occurrences_listed`, `total_days_listed`, `parse.confidence` | (no column) | **Missing in model** | Not stored in MVP; retrievable via `canonical_record_id`. Flagged for DATA_MODEL review (DEC-040) |
| Programme `topic_tags[]` (`ASSUMED`) | `CourseTopic` (`method='keyword_rule'`, `status='suggested'`) | Yes | Direct |
| Document records | `LearningMaterial`, `LearningMaterialTopic`, `Document` | Yes | Imported in Phase 5 with the content module, not Phase 2 |
| TPAC references | (not modelled) | Consistent | Not used by MVP ([MVP_SCOPE.md](MVP_SCOPE.md) §6) |

**Conventions confirmed from DATA_MODEL.md §1:** UUID primary keys generated by the database (`gen_random_uuid()`); `organization_id` on every tenant-scoped table; standard audit columns (`created_at`, `updated_at`, `created_by`, `updated_by`); soft delete by `status`; optimistic locking by `row_version` on OL tables; enumerations as `text` + `CHECK` (DEC-029); `AuditLog.id` is a `bigint` identity (documented exception).

**Embedding dimension:** undecided (DEC-006). No vector column is created before Phase 5 (DEC-038).

## 4. Referenced documents that do not exist

| Document | Referenced by | Status |
|---|---|---|
| `IMPLEMENTATION_ROADMAP.md` | PRD, MVP_SCOPE, FEATURE_CATALOG, DECISIONS | Generated 2026-09-14 (DEC-032) |
| `AGENT_CONTEXT.md` | PRD, MVP_SCOPE, TECH_STACK, DATA_MODEL, DECISIONS | Generated 2026-09-14 (DEC-032) |
| `ERROR_HANDLING_SPEC.md` | SYSTEM_ARCHITECTURE, API_INTEGRATION_SPEC, UI_UX_SPEC, MVP_SCOPE | Missing (DEC-039) |
| `TESTING_STRATEGY.md` | PRD, MVP_SCOPE, TECH_STACK, AI_SYSTEM_SPEC | Missing (DEC-039) |
| `OBSERVABILITY_SPEC.md` | PRD, SYSTEM_ARCHITECTURE, AI_SYSTEM_SPEC | Missing (DEC-039) |
| `DATA_PROVENANCE.md` | PRD, DATA_MODEL, SECURITY_RESPONSIBLE_AI | Missing (DEC-039) |
| `DOCUMENTATION_INDEX.md` | PRD, DECISIONS, FEATURE_CATALOG | Missing (DEC-039) |
| `ASSUMPTIONS_AND_OPEN_QUESTIONS.md` | PRD, DECISIONS, FEATURE_CATALOG | Missing (DEC-039) |
| `DOCUMENTATION_VALIDATION_REPORT.md` | FEATURE_CATALOG | Missing (DEC-039) |

## 5. Phase progress

| Roadmap phase | Status | Notes |
|---|---|---|
| 1 Discovery and data collection | Complete | Evidence in §1 and §2.5 |
| 2 Backend foundation and reference schema | **Complete for local development** | All Phase 2 exit criteria hold (below). Not done and not Phase 2 exit criteria: CI pipeline, separate database role for append-only grants, `scripts/` manifest |
| Vertical slice 1 (crosses 3, 4, 7, 8) | **Implemented on DEMO content** | Thin versions of MVP-01, 02, 03, 04, 06, 07, 08, 17, 19. No roadmap phase is complete; see exit-criteria gaps below |
| 3 Authentication, RBAC and audit | Partially implemented | Missing: password change/reset, re-auth, revoke-all, rate limiting, user administration, full authorisation matrix |
| 4 Competency engine and assessments | Partially implemented | Missing: framework/mapping administration, authoring, publishing, review, adjustments, corrections; blocked for real data by DEC-013, DEC-020 |
| 7 Recommendations and learning paths | Partially implemented | Missing: persistence, feedback, learning paths, progress |
| 8 Learner web application | Partially implemented | Missing: profile/settings, library, Q&A, progress, i18n, accessibility audit, Playwright journeys |
| 5, 6, 9–12 | Not started | — |

### Phase 2 exit criteria

| Criterion | Result | Evidence |
|---|---|---|
| `alembic upgrade head` on an empty database; `downgrade base` succeeds | Pass | `tests/db/test_migrations.py::test_downgrade_to_base_then_upgrade_again` |
| Models and migrations in sync | Pass | `tests/db/test_migrations.py::test_models_and_migrations_in_sync` |
| `/healthz` 200; `/readyz` 200 with a database and 503 without | Pass | `tests/unit/test_http_foundation.py`; `tests/db/test_migrations.py::test_readyz_ok_with_database` |
| Errors are problem+json with a correlation ID | Pass | `tests/unit/test_http_foundation.py` |
| Seed is idempotent, refuses INVALID, stores no CSCD definitions and no MOCK | Pass | `tests/db/test_seed.py`, including the CLI run twice |
| Database constraint tests | Pass | `tests/db/test_reference_schema.py` |
| Existing 35 tests pass | Pass | `python -m unittest discover -s tests -t .` |

### Vertical slice 1 - what is and is not done

| Requirement from the slice brief | Result | Evidence |
|---|---|---|
| Authentication (real, not demo-only) | Done: server-side sessions, CSRF, lockout | `tests/db/test_vertical_slice_api.py` (login, lockout, CSRF, logout, expiry, cookie flags) |
| Fetch competency framework data | Done for the selected job role | `GET /job-roles/{id}/competencies` |
| Submit an assessment | Done | journey test; live smoke `09`, `12` |
| Deterministic score calculation, no AI | Done (`score-v1`) | `tests/unit/test_scoring.py` (determinism, order independence, exhaustive small cases); journey asserts 1.00000 / 0.28571 / total 0.64286 |
| Skill-gap response | Done (band-gated) | `tests/unit/test_scoring.py::test_gap_rule`; journey test |
| Course recommendation response | Done (`rec-v1`) | `tests/unit/test_recommendation_rules.py`; journey test |
| One basic frontend flow consuming the APIs | Done; tested with mocked API and via proxy smoke; **not walked through in a browser** | `frontend/src/pages/pages.test.tsx`; `11`, `12` |
| Validation and clear errors on every endpoint | Done for slice endpoints | invalid-input and authorisation tests (48 API tests) |
| Demo functionality labelled | Done | `is_demo` in API, DEMO badges/banner, demo seed refused outside local/ci |
