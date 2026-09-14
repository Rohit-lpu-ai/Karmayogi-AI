# Implementation Status

| Field | Value |
|---|---|
| **Version** | 1.2.0 (after vertical slice 1) |
| **Last verified** | 2026-09-15 |
| **Verified on** | Branch `Diw`, HEAD `35d10a9`. **Everything after that commit is uncommitted**: the documentation package (staged/modified), `backend/`, `deploy/`, `frontend/` (untracked) |
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
| React application | Partially implemented | `frontend/` (React 18, TypeScript, Vite 8, React Router 7): login, get started (notice + job role), assessment, result, dashboard; 12 Vitest tests; production build. Not verified in a real browser |
| Design system, screens | Partially implemented | Plain CSS tokens (DEC-048); loading/empty/error states with correlation IDs; DEMO badges and banner. No Tailwind/shadcn, no i18n catalogue, no axe checks |

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
