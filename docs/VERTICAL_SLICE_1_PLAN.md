# Vertical Slice 1 - Plan and Pre-implementation Verification

| Field | Value |
|---|---|
| **Date** | 2026-09-15 |
| **Scope** | Login → role selection → assessment → deterministic scoring → gaps → course recommendations → basic learner dashboard |
| **Evidence** | Command output in [evidence/implementation/vertical-slice-1/](evidence/implementation/vertical-slice-1/) |
| **Related** | [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [DECISIONS.md](DECISIONS.md) DEC-045 to DEC-048 |

This slice cuts across roadmap Phases 3, 4, 7 and 8. It implements the thinnest version of each step. It is **not** the completion of any of those phases.

---

## A. Verification report of the existing backend foundation

Verified by re-running commands, not by reading the previous report.

| Claim (source) | Verified? | Evidence file |
|---|---|---|
| Migrations `0001`, `0002` at head; no model/migration drift (IMPLEMENTATION_STATUS §1a, DATA_MODEL §18) | Yes. `alembic current` = `0002 (head)`; `alembic check` = "No new upgrade operations detected" | `02-database-verification.txt`, `03-existing-tests.txt` |
| 16 reference tables, extensions `pgcrypto`, `citext`, no `vector` (DATA_MODEL §18, DEC-038) | Yes | `02` |
| 6 integrity triggers (restricted definition, restriction change, min-score order, required level, audit append-only ×2) | Yes | `02` |
| Seed: 23 topics, 1 framework, 4 clusters, 25 competencies, 5 levels, 100 source records, 99 courses, 111 course topics, 8 synthetic users, 1 department | Yes | `02` |
| No CSCD descriptions stored; framework `draft`, restricted, version `2014`; all courses `unreviewed` | Yes | `02` |
| Users have no passwords | Yes (0 of 8) | `02` |
| No job roles, role mappings or course-competency mappings | Yes (all 0) - **the slice cannot run on existing data** | `02` |
| 73 backend tests pass; 35 Phase 1 tests pass | Yes (73 passed; 35 OK) | `03` |
| Implemented routes: `/healthz`, `/readyz` only (API_INTEGRATION_SPEC status line) | Yes | `04-document-claim-checks.txt` |
| Local database `pgvector/pgvector:pg17` healthy on 127.0.0.1:5433 | Yes | `02` |
| `.env` and `backend/.venv` git-ignored | Yes | `04` |

**Discrepancies found:**

| Document | Stale or unverified statement | Fact |
|---|---|---|
| MVP_SCOPE.md §1 | "API paths … None exist yet"; "only IGOT-010 … have code" | Health endpoints and the reference schema exist |
| AGENT_CONTEXT.md §5 | "Backend application: In progress (Phase 2)" | Phase 2 complete for local development |
| IMPLEMENTATION_ROADMAP.md header | "Phase 2 in progress" | Phase 2 complete for local development |
| IMPLEMENTATION_STATUS.md | Does not state that Phases 2 and earlier documentation are **uncommitted** | `git status`: `backend/`, `deploy/` untracked; docs staged or modified; last commit is still `35d10a9` |
| IMPLEMENTATION_STATUS.md | "Startup check for synthetic users" is described as planned | Confirmed not implemented; only the seed refuses |

## B. Files and modules that already exist

| Area | Files |
|---|---|
| App and core | `backend/app/main.py`, `app/models.py`, `app/core/{config,db,errors,logging,middleware,vocab}.py` |
| Platform | `app/modules/platform/{api,models}.py` (health; Topic) |
| Organisation | `app/modules/organization/models.py` (Organization, Department, JobRole) |
| Identity | `app/modules/identity/models.py` (User, UserAccessRole) |
| Competency | `app/modules/competency/models.py` (CompetencyFramework, CompetencyCluster, Competency, CompetencyLevel, RoleCompetency) |
| Content | `app/modules/content/models.py` (SourceRecord) |
| Recommendation | `app/modules/recommendation/models.py` (Course, CourseTopic, CourseCompetency) |
| Governance | `app/modules/governance/{models,service}.py` (AuditLog, `record_audit`) |
| Seed | `app/seed/{__main__,canonical,importer,demo_users}.py` |
| Migrations | `migrations/env.py`, `versions/20260914_0001_extensions.py`, `versions/20260914_0002_reference_schema_…py` |
| Tests | `tests/conftest.py`, `tests/unit/{test_config,test_http_foundation,test_logging}.py`, `tests/db/{test_migrations,test_reference_schema,test_seed}.py` |
| Deploy | `deploy/docker-compose.yml`, `deploy/postgres/init/01-create-test-database.sql` |
| Phase 1 | `clients/`, `scripts/`, `data/`, `schemas/`, `tests/` (root) |
| Frontend | **None** |

## C. Missing pieces required for the slice

| Step | Missing |
|---|---|
| 1 Authentication | Session table; Argon2id hashing (`argon2-cffi`); login/logout/session endpoints; session cookie; CSRF; lockout; current-user dependency; basic role guard; demo passwords |
| 2 Role selection | Notice acknowledgement table and endpoint (MVP-03: no assessment before acknowledgement); job-role list; `PUT /me/job-role`; **a job role with approved competency mappings (none exist)** |
| 3 Assessment | Question, version and option tables; assessment, pool, attempt, delivered-question and answer tables; start/resume, save answer, submit; **approved questions (none exist)** |
| 4 Scoring | Evidence ledger and current-estimate tables; deterministic `score-v1` function; **level thresholds (CSCD levels have none)** |
| 5 Gaps | Gap rule over approved mappings and evidence bands |
| 6 Recommendations | Deterministic `rec-v1` function; **reviewed courses with approved competency mappings (none exist)** |
| 7 Dashboard | Frontend application (none exists) |

Because the bold items have no official source (DEC-013), the slice needs a **clearly labelled synthetic demo content seed** (DEC-045): one draft functional framework, two competencies, one job role, ten arithmetic items, one assessment and three internal courses. All names start with `DEMO`, and the seed runs only in `local` and `ci`.

## D. Database tables reused

| Table | Use in slice |
|---|---|
| `organizations` | Tenant of every query |
| `users` | Login (`password_hash`, `status`, `failed_login_count`, `locked_until`, `last_login_at`), `job_role_id` |
| `user_access_roles` | Role guard (auditor and platform_admin cannot take assessments) |
| `departments` | Unchanged (demo users already assigned) |
| `job_roles` | Role selection |
| `competency_frameworks`, `competencies`, `competency_levels` | Framework data, level thresholds |
| `role_competencies` | Approved required levels (gaps) |
| `courses`, `course_competencies` | Recommendation candidates (approved only) |
| `audit_logs` | `auth.*`, `user.job_role.change`, `attempt.submit`, `seed.import` |

**New tables (migration `0003`), all defined in DATA_MODEL.md:** `sessions`, `notice_acknowledgements`, `questions`, `question_versions`, `question_options`, `assessments`, `assessment_questions`, `assessment_attempts`, `attempt_questions`, `answers`, `competency_evidence`, `user_competencies`.

**Not created in this slice** (deliberately): `citations` (needs Phase 5 content tables), `review_tasks`, `approvals`, `user_competency_snapshots`, `recommendations`, `learning_paths`, `background_jobs`, `idempotency_keys`. Columns that would reference missing tables (`question_versions.ai_interaction_id`, `prompt_template_version_id`, `stem_embedding`; `questions.generation_job_id`) are omitted until their phase (DEC-046).

## E. API endpoints to be created

All under `/api/v1`, all return problem+json errors, all state-changing routes require `X-CSRF-Token`.

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/login` | Create session (public) |
| POST | `/auth/logout` | End session |
| GET | `/auth/session` | Session info and CSRF token |
| GET | `/me` | Profile, access roles, job role, notice state |
| POST | `/me/notice-acknowledgements` | Acknowledge privacy and AI-use notice |
| PUT | `/me/job-role` | Select job role |
| GET | `/job-roles` | Active job roles in the organisation |
| GET | `/job-roles/{id}/competencies` | Approved competency requirements with framework level scale |
| GET | `/assessments` | Published assessments for the caller's job role |
| POST | `/assessments/{id}/attempts` | Start or resume an attempt |
| GET | `/attempts/{id}` | Delivered questions without answer keys, saved answers |
| PUT | `/attempts/{id}/answers/{question_version_id}` | Save one answer |
| POST | `/attempts/{id}/submit` | Score deterministically, write evidence, recompute estimates |
| GET | `/attempts/{id}/result` | Per-competency result and per-question feedback |
| GET | `/me/competency-profile` | Estimates with evidence band and explanation |
| GET | `/me/competency-gaps` | Gaps, strengths, "reassess to confirm" |
| GET | `/me/recommendations` | Deterministic course recommendations with reasons |

## F. Frontend pages and components

`frontend/` - React + TypeScript + Vite, React Router, plain CSS tokens (DEC-048).

| Page | API calls |
|---|---|
| Login | `POST /auth/login`, `GET /auth/session` |
| Get started (notice + job role) | `GET /me`, `POST /me/notice-acknowledgements`, `GET /job-roles`, `GET /job-roles/{id}/competencies`, `PUT /me/job-role` |
| Assessment | `GET /assessments`, `POST /assessments/{id}/attempts`, `GET /attempts/{id}`, `PUT …/answers/…`, `POST …/submit` |
| Result | `GET /attempts/{id}/result` |
| Dashboard | `GET /me`, `GET /me/competency-profile`, `GET /me/competency-gaps`, `GET /me/recommendations` |

Components: `AppShell` (header, sign out, DEMO environment banner), `DemoBadge`, `LoadingState` / `ErrorState` / `EmptyState` (show problem `code` and correlation ID), API client (credentials, CSRF header, problem parsing), auth context, route guard.

## G. Test plan

| Layer | Tests |
|---|---|
| Unit (pure) | `score-v1`: weights, level mapping, null thresholds, bands at 2/3/4/5/9/10 items, determinism (same input → same output, input order irrelevant); gap rule (band gating, missing level, strength); `rec-v1`: ranking, tie-breaks, dedup across gaps, unapproved excluded; password hashing; CSRF token binding; attempt order reproducible from seed |
| Migration / database | `0003` upgrade, downgrade, model sync; append-only triggers on question versions, options, delivered questions, evidence; evidence void columns set-once; one baseline per user |
| API (normal) | Full journey: login → session → notice → job role → start → resume returns same attempt → answer → submit → result → profile → gaps → recommendations |
| API (invalid input) | Bad email/empty password (422), wrong password (401 generic), lockout after N failures (423 `ACCOUNT_LOCKED`), unknown job role (404), inactive role, option not belonging to question (422), answer after submit (409), double submit (409), start without notice (409 `NOTICE_NOT_ACKNOWLEDGED`), start without job role (409), non-UUID path (422), extra body fields (422) |
| Authorisation | Every slice endpoint without session → 401; state change without/with wrong CSRF → 403; other user's attempt → 404; other organisation's job role → 404; auditor and platform_admin cannot start assessments → 403; expired and revoked sessions → 401 |
| Key leakage | No `is_correct` or correct option in start, get-attempt or save-answer responses |
| Demo labelling | Every demo framework, competency, question, assessment and course response carries `is_demo: true`; demo seed refused outside `local`/`ci` |
| Frontend | Vitest + Testing Library: API client (CSRF header, problem parsing), dashboard renders gaps/recommendations with DEMO labels, assessment page never renders keys; `tsc` type-check and production build |
| Live smoke | uvicorn + real database: scripted HTTP journey; Vite production build |

## H. Architectural conflicts and risky assumptions

| # | Issue | Handling |
|---|---|---|
| H-1 | No official functional framework, role mapping, approved questions or reviewed course mappings exist (DEC-013) | Synthetic `DEMO` seed, local/ci only, every API object flagged `is_demo` (DEC-045). Nothing is presented as official |
| H-2 | Demo "approvals" of mappings, questions and courses are performed by the seed, not by a human reviewer; no `ReviewTask`/`Approval` records exist; invariant M-11 is not met for demo items | Recorded as demo-only; items use `origin='demo_seed'` (DEC-046). Real questions still require Phase 4/6 review |
| H-3 | Demo questions have no citations (the citation table depends on Phase 5 content tables) | Items are self-contained arithmetic with a mathematically certain key; labelled "synthetic arithmetic, not an official assessment question" |
| H-4 | Spec recomputes estimates in a background job; no job infrastructure exists (DEC-035) | Recompute synchronously inside the submit transaction (DEC-047) |
| H-5 | Spec persists `Recommendation` rows with feedback | Computed on read, deterministic, no persistence, no dismiss feedback yet (DEC-047) |
| H-6 | `Idempotency-Key` required on submit; `IdempotencyKey` table absent | Submit is guarded by attempt state (second submit → 409); header not enforced yet (DEC-047) |
| H-7 | Email is unique per organisation, not globally; login needs an organisation | Optional `organization_code`; without it, login succeeds only if exactly one organisation has that email (DEC-047) |
| H-8 | CSRF token storage is not modelled in `Session` | Token = HMAC-SHA256(`SESSION_SECRET`, raw session token): bound to the session, no extra column (DEC-047) |
| H-9 | Failed logins for unknown emails cannot be written to the tenant-scoped `audit_logs` (no organisation) | Logged as a redacted application warning only |
| H-10 | Baseline snapshots (`user_competency_snapshots`) not created | `assessment_attempts.is_baseline` set on the first scored pre attempt; history view deferred |
| H-11 | Privacy and AI-use notice text is not legally approved (DEC-027) | Notice version `privacy-ai-use-draft-0`, text labelled DRAFT |
| H-12 | TECH_STACK proposes Tailwind, shadcn/ui and TanStack Query | Not adopted in this slice to keep dependencies minimal (DEC-048); revisit in Phase 8 |
| H-13 | Rate limiting (SEC-014) needs a store; Redis absent | Account lockout implemented; IP rate limiting deferred |
| H-14 | Retaking a `pre` assessment is post-assessment behaviour (P1) | A second attempt after scoring is refused (409 `ASSESSMENT_ALREADY_COMPLETED`) |
| H-15 | Secure cookies are not sent over plain `http://testserver` | `SESSION_COOKIE_SECURE` must be true outside `local`/`ci` (startup validation) |
| H-16 | All work since commit `35d10a9` is uncommitted | Flagged; commit on request |
